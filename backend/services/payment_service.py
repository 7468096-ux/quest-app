from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx
import structlog

logger = structlog.get_logger(__name__)

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
TELEGRAM_STARS_PROVIDER_TOKEN = os.getenv("TELEGRAM_STARS_PROVIDER_TOKEN")


class PaymentService:
    async def create_invoice(self, provider: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if provider == "stripe":
            return await self._create_stripe_checkout(payload)
        if provider == "telegram_stars":
            return self._create_telegram_invoice(payload)
        raise ValueError(f"Unsupported provider: {provider}")

    async def handle_webhook(self, provider: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if provider == "stripe":
            return await self._handle_stripe_webhook(payload)
        if provider == "telegram_stars":
            return self._handle_telegram_payment(payload)
        raise ValueError(f"Unsupported provider: {provider}")

    async def _create_stripe_checkout(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not STRIPE_SECRET_KEY:
            raise RuntimeError("STRIPE_SECRET_KEY not set")
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.stripe.com/v1/checkout/sessions",
                headers={"Authorization": f"Bearer {STRIPE_SECRET_KEY}"},
                data={
                    "mode": "subscription",
                    "success_url": payload["success_url"],
                    "cancel_url": payload["cancel_url"],
                    "line_items[0][price]": payload["price_id"],
                    "line_items[0][quantity]": 1,
                    "customer_email": payload.get("email"),
                },
            )
            resp.raise_for_status()
            data = resp.json()
            logger.info("stripe_checkout_created", session_id=data.get("id"))
            return {"checkout_url": data.get("url"), "session_id": data.get("id")}

    async def _handle_stripe_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        event_type = payload.get("type")
        data = payload.get("data", {})
        logger.info("stripe_webhook_received", event_type=event_type)
        return {"event_type": event_type, "data": data}

    def _create_telegram_invoice(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not TELEGRAM_STARS_PROVIDER_TOKEN:
            raise RuntimeError("TELEGRAM_STARS_PROVIDER_TOKEN not set")
        invoice = {
            "title": payload["title"],
            "description": payload["description"],
            "payload": payload["payload"],
            "provider_token": TELEGRAM_STARS_PROVIDER_TOKEN,
            "currency": payload.get("currency", "USD"),
            "prices": payload["prices"],
        }
        return invoice

    def _handle_telegram_payment(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("telegram_payment_success", payload=payload.get("payload"))
        return {"status": "ok", "payload": payload}


payment_service = PaymentService()
