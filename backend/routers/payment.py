"""Payment router — Stripe webhooks + Telegram Stars invoice generation.

Environment variables required (set in .env when deploying):
  STRIPE_SECRET_KEY          — Stripe secret key (sk_live_... or sk_test_...)
  STRIPE_WEBHOOK_SECRET      — Stripe webhook signing secret (whsec_...)
  TELEGRAM_STARS_TOKEN       — Telegram Stars provider token (from @BotFather)

Routes:
  POST /api/payment/invoice          — Create a payment invoice (Stripe or Stars)
  POST /api/payment/webhook/stripe   — Stripe webhook handler
  POST /api/payment/webhook/stars    — Telegram Stars successful_payment handler
  GET  /api/payment/status/{bot_id}  — Current subscription status for authenticated user
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Literal, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config_loader import get_bot_config
from backend.models.database import Subscription, User, get_session
from backend.routers.auth import get_current_user

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/payment", tags=["payment"])

# ---------------------------------------------------------------------------
# Config from env
# ---------------------------------------------------------------------------

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
TELEGRAM_STARS_TOKEN = os.getenv("TELEGRAM_STARS_TOKEN", "")

# Plan durations (days)
PLAN_DURATION: dict[str, int] = {
    "basic": 30,
    "pro": 30,
}

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class InvoiceRequest(BaseModel):
    bot_id: str
    plan: Literal["basic", "pro"]
    provider: Literal["stripe", "telegram_stars"] = "stripe"
    # Optional: override success/cancel redirect for Stripe Checkout
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None


class InvoiceResponse(BaseModel):
    provider: str
    invoice_url: Optional[str] = None        # Stripe Checkout URL
    invoice_payload: Optional[str] = None    # Telegram Stars payload (for bot)
    stars_amount: Optional[int] = None       # Stars price (for bot to send_invoice)
    title: Optional[str] = None
    description: Optional[str] = None


class SubscriptionStatus(BaseModel):
    bot_id: str
    plan: str
    status: str
    expires_at: Optional[str] = None
    questions_per_day: Optional[int] = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_plan_price_usd(config, plan: str) -> float:
    tier = getattr(config.pricing, plan, None)
    if tier is None:
        raise HTTPException(status_code=400, detail=f"Plan '{plan}' not found in bot config")
    return float(getattr(tier, "price_usd", 0))


def _usd_to_stars(price_usd: float) -> int:
    """Convert USD price to Telegram Stars (approximate: 1 star ≈ $0.013).
    
    Official rate from Telegram docs: 50 stars = $1, so 1 USD = 77 stars ≈ 80 stars.
    We round up to nearest multiple of 5.
    """
    stars = price_usd * 77
    return max(int((stars + 4) // 5 * 5), 5)  # round up to nearest 5


async def _upsert_subscription(
    session: AsyncSession,
    user_id: uuid.UUID,
    bot_id: str,
    plan: str,
    provider: str,
    payment_id: str,
    price_usd: float,
    currency: str = "USD",
) -> Subscription:
    """Create or upgrade subscription after successful payment."""
    result = await session.execute(
        select(Subscription).where(Subscription.user_id == user_id, Subscription.bot_id == bot_id)
    )
    sub = result.scalar_one_or_none()

    duration_days = PLAN_DURATION.get(plan, 30)
    expires = datetime.utcnow() + timedelta(days=duration_days)

    if sub:
        sub.plan = plan
        sub.status = "active"
        sub.payment_provider = provider
        sub.payment_id = payment_id
        sub.price_usd = price_usd
        sub.currency = currency
        sub.expires_at = expires
        sub.started_at = datetime.utcnow()
    else:
        sub = Subscription(
            user_id=user_id,
            bot_id=bot_id,
            plan=plan,
            status="active",
            payment_provider=provider,
            payment_id=payment_id,
            price_usd=price_usd,
            currency=currency,
            expires_at=expires,
        )
        session.add(sub)

    await session.flush()
    return sub


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.post("/invoice", response_model=InvoiceResponse)
async def create_invoice(
    payload: InvoiceRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> InvoiceResponse:
    """Generate a payment link (Stripe Checkout or Telegram Stars invoice params)."""

    config = get_bot_config(payload.bot_id)
    if not config:
        raise HTTPException(status_code=404, detail="Bot not found")

    price_usd = _get_plan_price_usd(config, payload.plan)

    if payload.provider == "stripe":
        if not STRIPE_SECRET_KEY:
            raise HTTPException(status_code=503, detail="Stripe not configured (STRIPE_SECRET_KEY missing)")

        try:
            import stripe  # noqa: PLC0415
            stripe.api_key = STRIPE_SECRET_KEY
        except ImportError as exc:
            raise HTTPException(status_code=503, detail="stripe library not installed") from exc

        price_cents = int(price_usd * 100)
        session_obj = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": price_cents,
                        "product_data": {
                            "name": f"{config.name} — {payload.plan.capitalize()} Plan",
                            "description": f"30-day {payload.plan} subscription for {config.name}",
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={
                "user_id": str(current_user.id),
                "bot_id": payload.bot_id,
                "plan": payload.plan,
            },
            success_url=payload.success_url or "https://smarthelp.ai/payment/success",
            cancel_url=payload.cancel_url or "https://smarthelp.ai/payment/cancel",
        )
        logger.info("stripe_checkout_created", session_id=session_obj.id, user_id=str(current_user.id))
        return InvoiceResponse(
            provider="stripe",
            invoice_url=session_obj.url,
            title=f"{config.name} {payload.plan.capitalize()}",
        )

    elif payload.provider == "telegram_stars":
        # Return invoice parameters to be used by the Telegram bot (send_invoice call)
        stars = _usd_to_stars(price_usd)
        payload_str = json.dumps({
            "user_id": str(current_user.id),
            "bot_id": payload.bot_id,
            "plan": payload.plan,
        })
        return InvoiceResponse(
            provider="telegram_stars",
            stars_amount=stars,
            invoice_payload=payload_str,
            title=f"{config.name} — {payload.plan.capitalize()}",
            description=f"30-day {payload.plan} subscription. {int(price_usd)} USD",
        )

    raise HTTPException(status_code=400, detail="Unknown provider")


@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, session: AsyncSession = Depends(get_session)):
    """Handle Stripe webhook events (checkout.session.completed, payment_intent.succeeded)."""

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Stripe webhook not configured")

    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature", "")

    try:
        import stripe  # noqa: PLC0415
        stripe.api_key = STRIPE_SECRET_KEY
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ImportError as exc:
        raise HTTPException(status_code=503, detail="stripe library not installed") from exc
    except Exception as exc:
        logger.warning("stripe_webhook_signature_invalid", error=str(exc))
        raise HTTPException(status_code=400, detail="Invalid signature") from exc

    if event["type"] == "checkout.session.completed":
        obj = event["data"]["object"]
        meta = obj.get("metadata", {})
        user_id_str = meta.get("user_id")
        bot_id = meta.get("bot_id")
        plan = meta.get("plan")

        if not all([user_id_str, bot_id, plan]):
            logger.warning("stripe_webhook_missing_metadata", event_id=event["id"])
            return {"ok": True}

        try:
            user_uuid = uuid.UUID(user_id_str)
        except ValueError:
            logger.warning("stripe_webhook_invalid_user_id", user_id=user_id_str)
            return {"ok": True}

        price_usd = (obj.get("amount_total") or 0) / 100.0
        await _upsert_subscription(
            session,
            user_id=user_uuid,
            bot_id=bot_id,
            plan=plan,
            provider="stripe",
            payment_id=obj["id"],
            price_usd=price_usd,
        )
        await session.commit()
        logger.info(
            "stripe_subscription_activated",
            user_id=user_id_str,
            bot_id=bot_id,
            plan=plan,
            price_usd=price_usd,
        )

    return {"ok": True}


@router.post("/webhook/stars")
async def telegram_stars_webhook(request: Request, session: AsyncSession = Depends(get_session)):
    """Handle Telegram Stars successful_payment update forwarded by the bot runner.

    The bot runner (telegram/bot_runner.py) should forward successful_payment updates here.
    Expected body: {
        "telegram_id": int,
        "payment_payload": "<json string with user_id, bot_id, plan>",
        "telegram_payment_charge_id": str,
        "total_amount": int   # in stars
    }
    """
    body = await request.json()

    telegram_id: Optional[int] = body.get("telegram_id")
    payment_payload_str: Optional[str] = body.get("payment_payload")
    charge_id: Optional[str] = body.get("telegram_payment_charge_id")
    total_amount: int = body.get("total_amount", 0)

    if not all([telegram_id, payment_payload_str, charge_id]):
        raise HTTPException(status_code=400, detail="Missing required fields")

    try:
        payment_data = json.loads(payment_payload_str)
        bot_id = payment_data["bot_id"]
        plan = payment_data["plan"]
        user_id_str = payment_data.get("user_id")
    except (json.JSONDecodeError, KeyError) as exc:
        raise HTTPException(status_code=400, detail="Invalid payment payload") from exc

    # Lookup user
    user = None
    if user_id_str:
        try:
            result = await session.execute(select(User).where(User.id == uuid.UUID(user_id_str)))
            user = result.scalar_one_or_none()
        except (ValueError, Exception):
            pass

    if user is None and telegram_id:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Stars → approximate USD
    price_usd = round(total_amount / 77.0, 2)

    await _upsert_subscription(
        session,
        user_id=user.id,
        bot_id=bot_id,
        plan=plan,
        provider="telegram_stars",
        payment_id=charge_id,
        price_usd=price_usd,
        currency="XTR",  # ISO code for Telegram Stars
    )
    await session.commit()

    logger.info(
        "stars_subscription_activated",
        user_id=str(user.id),
        telegram_id=telegram_id,
        bot_id=bot_id,
        plan=plan,
        stars=total_amount,
    )
    return {"ok": True}


@router.get("/status/{bot_id}", response_model=SubscriptionStatus)
async def subscription_status(
    bot_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> SubscriptionStatus:
    """Return current subscription status for the authenticated user + bot."""

    config = get_bot_config(bot_id)
    if not config:
        raise HTTPException(status_code=404, detail="Bot not found")

    result = await session.execute(
        select(Subscription).where(
            Subscription.user_id == current_user.id,
            Subscription.bot_id == bot_id,
        )
    )
    sub = result.scalar_one_or_none()

    if not sub:
        # Return default free tier (no DB row)
        return SubscriptionStatus(
            bot_id=bot_id,
            plan="free",
            status="active",
            expires_at=None,
            questions_per_day=getattr(getattr(config.pricing, "free", None), "questions_per_day", 5),
        )

    # Check expiry
    if sub.expires_at and sub.expires_at < datetime.utcnow() and sub.plan != "free":
        sub.plan = "free"
        sub.status = "expired"
        await session.commit()

    plan_config = getattr(config.pricing, sub.plan, None)
    qpd = getattr(plan_config, "questions_per_day", None) if plan_config else None
    if isinstance(qpd, str) and qpd == "unlimited":
        qpd = None  # None = unlimited in SubscriptionStatus

    return SubscriptionStatus(
        bot_id=bot_id,
        plan=sub.plan,
        status=sub.status,
        expires_at=sub.expires_at.isoformat() if sub.expires_at else None,
        questions_per_day=qpd,
    )
