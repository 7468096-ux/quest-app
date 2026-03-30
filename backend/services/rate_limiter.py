from __future__ import annotations

from datetime import date
from typing import Tuple
import uuid

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.database import UsageLog

logger = structlog.get_logger(__name__)


async def check_and_increment(
    session: AsyncSession,
    user_id: uuid.UUID,
    bot_id: str,
    daily_limit: int | None,
) -> Tuple[bool, int | None]:
    if daily_limit is None:
        return True, None

    today = date.today()
    result = await session.execute(
        select(UsageLog).where(UsageLog.user_id == user_id, UsageLog.bot_id == bot_id, UsageLog.date == today)
    )
    usage = result.scalar_one_or_none()

    if usage is None:
        usage = UsageLog(user_id=user_id, bot_id=bot_id, date=today, questions_count=0)
        session.add(usage)

    if usage.questions_count >= daily_limit:
        remaining = 0
        return False, remaining

    usage.questions_count += 1
    remaining = max(daily_limit - usage.questions_count, 0)
    logger.info("rate_limit_increment", user_id=user_id, bot_id=bot_id, remaining=remaining)
    return True, remaining
