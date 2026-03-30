from __future__ import annotations

import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Header, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.database import Subscription, User, get_session

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api", tags=["auth"])

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "43200"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TelegramAuthRequest(BaseModel):
    telegram_id: int
    name: Optional[str] = None
    language: Optional[str] = None
    country_code: Optional[str] = None
    bot_id: Optional[str] = None


class WebAuthRequest(BaseModel):
    email: EmailStr
    password: str
    language: Optional[str] = None
    country_code: Optional[str] = None


class AuthResponse(BaseModel):
    user_id: str
    token: str


class MeResponse(BaseModel):
    id: str
    email: Optional[str]
    telegram_id: Optional[int]
    name: Optional[str]
    language: Optional[str]
    country_code: Optional[str]


def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
) -> User:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    try:
        user_uuid = uuid.UUID(user_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    result = await session.execute(select(User).where(User.id == user_uuid))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.post("/auth/telegram", response_model=AuthResponse)
async def auth_telegram(payload: TelegramAuthRequest, session: AsyncSession = Depends(get_session)) -> AuthResponse:
    result = await session.execute(select(User).where(User.telegram_id == payload.telegram_id))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            telegram_id=payload.telegram_id,
            name=payload.name,
            language=payload.language,
            country_code=payload.country_code,
        )
        session.add(user)
        await session.flush()

    if payload.bot_id:
        sub_result = await session.execute(
            select(Subscription).where(Subscription.user_id == user.id, Subscription.bot_id == payload.bot_id)
        )
        subscription = sub_result.scalar_one_or_none()
        if not subscription:
            session.add(Subscription(user_id=user.id, bot_id=payload.bot_id, plan="free", status="active"))

    token = create_access_token(str(user.id))
    await session.commit()
    return AuthResponse(user_id=str(user.id), token=token)


@router.post("/auth/web", response_model=AuthResponse)
async def auth_web(payload: WebAuthRequest, session: AsyncSession = Depends(get_session)) -> AuthResponse:
    result = await session.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if user:
        if not user.hashed_password or not pwd_context.verify(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    else:
        user = User(
            email=payload.email,
            hashed_password=pwd_context.hash(payload.password),
            language=payload.language,
            country_code=payload.country_code,
        )
        session.add(user)
        await session.flush()

    token = create_access_token(str(user.id))
    await session.commit()
    return AuthResponse(user_id=str(user.id), token=token)


@router.get("/me", response_model=MeResponse)
async def me(current_user: User = Depends(get_current_user)) -> MeResponse:
    return MeResponse(
        id=str(current_user.id),
        email=current_user.email,
        telegram_id=current_user.telegram_id,
        name=current_user.name,
        language=current_user.language,
        country_code=current_user.country_code,
    )
