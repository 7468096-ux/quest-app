from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend import config_loader
from backend.config_loader import BOTS_DIR, get_all_configs
from backend.routers import auth, chat, payment
from backend.routers import web as web_router
from backend.models.database import init_db
from backend.services.rag_engine import rag_engine

logger = structlog.get_logger(__name__)

_WEB_STATIC = Path(__file__).resolve().parents[1] / "web" / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("app_startup")
    await init_db()
    config_loader.reload_configs()
    await rag_engine.initialize(get_all_configs(), BOTS_DIR)
    yield
    logger.info("app_shutdown")


def create_app() -> FastAPI:
    app = FastAPI(title="AI Bots Platform", version="0.1.0", lifespan=lifespan)

    allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in allowed_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API routers (prefix /api)
    app.include_router(auth.router)
    app.include_router(chat.router)
    app.include_router(payment.router)

    # Static files (CSS, JS, images)
    if _WEB_STATIC.exists():
        app.mount("/static", StaticFiles(directory=str(_WEB_STATIC)), name="static")

    # Web landing pages — must be added AFTER /api routes
    app.include_router(web_router.router)

    return app


app = create_app()
