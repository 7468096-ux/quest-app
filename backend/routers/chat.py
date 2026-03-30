from __future__ import annotations

from datetime import datetime, date
import uuid
from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config_loader import get_bot_config
from backend.models.database import Conversation, Subscription, UsageLog, User, get_session
from backend.services.llm_router import route_llm
from backend.services.rag_engine import rag_engine
from backend.services.rate_limiter import check_and_increment

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    bot_id: str
    user_id: str
    message: str
    channel: str


class ChatResponse(BaseModel):
    response: str
    tokens_used: int
    remaining_questions_today: Optional[int]


def _get_plan_limit(config: any, plan: str) -> Optional[int]:
    tier = getattr(config.pricing, plan, None)
    if not tier:
        return None
    limit = tier.questions_per_day
    if isinstance(limit, str) and limit == "unlimited":
        return None
    if isinstance(limit, int):
        return limit
    return None


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, session: AsyncSession = Depends(get_session)) -> ChatResponse:
    config = get_bot_config(payload.bot_id)
    if not config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bot not found")

    user = None
    try:
        user_uuid = uuid.UUID(payload.user_id)
    except ValueError:
        user_uuid = None

    if user_uuid:
        user_result = await session.execute(select(User).where(User.id == user_uuid))
        user = user_result.scalar_one_or_none()
    else:
        try:
            telegram_id = int(payload.user_id)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id") from exc

        user_result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    sub_result = await session.execute(
        select(Subscription).where(Subscription.user_id == user.id, Subscription.bot_id == payload.bot_id)
    )
    subscription = sub_result.scalar_one_or_none()
    if not subscription:
        subscription = Subscription(user_id=user.id, bot_id=payload.bot_id, plan="free", status="active")
        session.add(subscription)
        await session.flush()

    if subscription.expires_at and subscription.expires_at < datetime.utcnow():
        subscription.status = "expired"
        subscription.plan = "free"

    plan_limit = _get_plan_limit(config, subscription.plan)
    allowed, remaining = await check_and_increment(session, user.id, payload.bot_id, plan_limit)
    if not allowed:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Daily limit reached")

    history: list[dict] = []
    conv_result = await session.execute(
        select(Conversation)
        .where(Conversation.user_id == user.id, Conversation.bot_id == payload.bot_id)
        .order_by(desc(Conversation.updated_at), desc(Conversation.created_at))
        .limit(1)
    )
    latest = conv_result.scalar_one_or_none()
    if latest and isinstance(latest.messages, list):
        history = latest.messages[-10:]

    rag_chunks = await rag_engine.get_relevant_chunks(payload.bot_id, payload.message, top_k=3)
    response_text, usage = await route_llm(config, subscription.plan, rag_chunks, history, payload.message)

    if config.niche.requires_disclaimer and config.disclaimer:
        disclaimer = config.disclaimer.strip()
        if disclaimer and disclaimer.lower() not in response_text.lower():
            response_text = f"{response_text}\n\n{disclaimer}"

    new_messages = history + [
        {"role": "user", "content": payload.message, "timestamp": datetime.utcnow().isoformat()},
        {"role": "assistant", "content": response_text, "timestamp": datetime.utcnow().isoformat()},
    ]

    if latest:
        latest.messages = new_messages
        latest.tokens_used = (latest.tokens_used or 0) + usage.get("prompt_tokens", 0) + usage.get("completion_tokens", 0)
        latest.updated_at = datetime.utcnow()
    else:
        conversation = Conversation(
            user_id=user.id,
            bot_id=payload.bot_id,
            channel=payload.channel,
            messages=new_messages,
            tokens_used=usage.get("prompt_tokens", 0) + usage.get("completion_tokens", 0),
            updated_at=datetime.utcnow(),
        )
        session.add(conversation)

    usage_result = await session.execute(
        select(UsageLog).where(
            UsageLog.user_id == user.id, UsageLog.bot_id == payload.bot_id, UsageLog.date == date.today()
        )
    )
    usage_log = usage_result.scalar_one_or_none()
    if usage_log:
        usage_log.tokens_input = (usage_log.tokens_input or 0) + usage.get("prompt_tokens", 0)
        usage_log.tokens_output = (usage_log.tokens_output or 0) + usage.get("completion_tokens", 0)
        usage_log.llm_model = usage.get("model")

    await session.commit()

    tokens_used = usage.get("prompt_tokens", 0) + usage.get("completion_tokens", 0)
    return ChatResponse(response=response_text, tokens_used=tokens_used, remaining_questions_today=remaining)
