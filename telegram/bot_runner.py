#!/usr/bin/env python3
"""Telegram Multi-Bot Runner.

Loads all bot configs and runs all Telegram bots in a single process.
Each bot has its own token and handlers but shares the API backend.
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Any

import httpx
import structlog
import yaml
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

logger = structlog.get_logger()

API_URL = os.environ.get("API_URL", "http://localhost:8000")
BOTS_DIR = Path(os.environ.get("BOTS_DIR", "/app/bots"))


def load_bot_configs() -> list[dict[str, Any]]:
    """Scan bots/ directory and load all configs with telegram tokens."""
    configs = []
    for config_path in sorted(BOTS_DIR.glob("*/config.yaml")):
        try:
            config = yaml.safe_load(config_path.read_text())
            bot_id = config.get("bot_id", config_path.parent.name)
            
            # Token from config or environment variable
            token_ref = config.get("telegram", {}).get("bot_token", "")
            if token_ref.startswith("${") and token_ref.endswith("}"):
                env_var = token_ref[2:-1]
                token = os.environ.get(env_var, "")
            else:
                token = token_ref
            
            if not token:
                logger.warning("no_telegram_token", bot_id=bot_id)
                continue
            
            config["_bot_id"] = bot_id
            config["_token"] = token
            config["_config_path"] = str(config_path)
            configs.append(config)
            logger.info("bot_config_loaded", bot_id=bot_id)
        except Exception as exc:
            logger.error("config_load_error", path=str(config_path), error=str(exc))
    
    return configs


async def api_call(endpoint: str, payload: dict) -> dict:
    """Make async call to the API backend."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{API_URL}{endpoint}", json=payload)
        resp.raise_for_status()
        return resp.json()


def make_handlers(config: dict):
    """Create handler functions bound to a specific bot config."""
    bot_id = config["_bot_id"]
    welcome = config.get("telegram", {}).get("welcome_message", f"Welcome to {config.get('name', bot_id)}!")
    pricing = config.get("pricing", {})
    
    async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command."""
        user = update.effective_user
        if not user:
            return
        
        # Register user via API
        try:
            await api_call("/api/auth/telegram", {
                "telegram_id": user.id,
                "name": user.full_name or user.first_name or "User",
                "language": config.get("country", {}).get("language", "en"),
                "bot_id": bot_id,
            })
        except Exception as exc:
            logger.error("auth_error", bot_id=bot_id, user_id=user.id, error=str(exc))
        
        await update.message.reply_text(welcome)
    
    async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle text messages — main chat flow."""
        user = update.effective_user
        if not user or not update.message or not update.message.text:
            return
        
        # Show typing indicator
        await update.message.chat.send_action("typing")
        
        try:
            result = await api_call("/api/chat", {
                "bot_id": bot_id,
                "user_id": str(user.id),
                "message": update.message.text,
                "channel": "telegram",
            })
            
            response_text = result.get("response", "Sorry, something went wrong.")
            remaining = result.get("remaining_questions_today")
            
            # Add remaining counter for free users
            if remaining is not None and remaining <= 3 and remaining >= 0:
                response_text += f"\n\n📊 {remaining} questions remaining today."
            
            # If limit exceeded
            if result.get("limit_exceeded"):
                basic_price = pricing.get("basic", {}).get("price_usd", 9)
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(f"⭐ Upgrade to Basic (${basic_price}/mo)", callback_data="upgrade_basic")],
                    [InlineKeyboardButton("🚀 Upgrade to Pro", callback_data="upgrade_pro")],
                ])
                await update.message.reply_text(
                    result.get("response", "Daily limit reached. Upgrade for more questions!"),
                    reply_markup=keyboard,
                )
                return
            
            await update.message.reply_text(response_text)
            
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                await update.message.reply_text("⏳ Too many requests. Please wait a moment.")
            else:
                logger.error("chat_api_error", bot_id=bot_id, status=exc.response.status_code)
                await update.message.reply_text("❌ Service temporarily unavailable. Please try again later.")
        except Exception as exc:
            logger.error("chat_error", bot_id=bot_id, error=str(exc))
            await update.message.reply_text("❌ An error occurred. Please try again.")
    
    async def plan_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /plan command — show current plan and upgrade options."""
        user = update.effective_user
        if not user:
            return
        
        try:
            result = await api_call(f"/api/usage/{bot_id}", {
                "user_id": str(user.id),
            })
            plan = result.get("plan", "free")
            used = result.get("questions_today", 0)
            limit = result.get("questions_limit", 3)
            
            basic = pricing.get("basic", {})
            pro = pricing.get("pro", {})
            
            text = (
                f"📋 Your current plan: **{plan.upper()}**\n"
                f"📊 Used today: {used}/{limit if limit > 0 else '∞'} questions\n\n"
                f"Available plans:\n"
                f"🆓 Free — {pricing.get('free', {}).get('questions_per_day', 3)} questions/day\n"
                f"⭐ Basic — ${basic.get('price_usd', 9)}/mo — {basic.get('questions_per_day', 30)} questions/day\n"
                f"🚀 Pro — ${pro.get('price_usd', 19)}/mo — Unlimited\n"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"⭐ Basic (${basic.get('price_usd', 9)}/mo)", callback_data="upgrade_basic")],
                [InlineKeyboardButton(f"🚀 Pro (${pro.get('price_usd', 19)}/mo)", callback_data="upgrade_pro")],
            ])
            
            await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")
        except Exception as exc:
            logger.error("plan_error", bot_id=bot_id, error=str(exc))
            await update.message.reply_text("Could not load plan info. Please try again.")
    
    async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command."""
        niche = config.get("niche", {}).get("type", "assistant")
        text = (
            f"ℹ️ I'm an AI {niche} assistant.\n\n"
            f"Commands:\n"
            f"/start — Start the bot\n"
            f"/plan — View your plan & upgrade\n"
            f"/help — This message\n\n"
            f"Just type your question and I'll help! 💬"
        )
        await update.message.reply_text(text)
    
    async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle inline button callbacks (upgrade, etc.)."""
        query = update.callback_query
        if not query:
            return
        await query.answer()
        
        user = update.effective_user
        data = query.data
        
        if data in ("upgrade_basic", "upgrade_pro"):
            plan = "basic" if data == "upgrade_basic" else "pro"
            price_info = pricing.get(plan, {})
            
            # For now, direct to Telegram Stars payment
            text = (
                f"To upgrade to **{plan.upper()}** (${price_info.get('price_usd', 0)}/mo):\n\n"
                f"💫 Pay via Telegram Stars — tap the button below\n"
                f"💳 Or visit: https://smarthelp.ai/pay/{bot_id}/{plan}\n"
            )
            
            # TODO: Implement Telegram Stars invoice creation
            # For MVP, link to web payment
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    f"💳 Pay ${price_info.get('price_usd', 0)}/mo",
                    url=f"https://smarthelp.ai/pay/{bot_id}/{plan}"
                )],
            ])
            
            await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")
    
    return start_handler, message_handler, plan_handler, help_handler, callback_handler


async def run_all_bots():
    """Load all bot configs and run all Telegram bots concurrently."""
    configs = load_bot_configs()
    
    if not configs:
        logger.error("no_bots_configured")
        sys.exit(1)
    
    applications = []
    
    for config in configs:
        bot_id = config["_bot_id"]
        token = config["_token"]
        
        start_h, message_h, plan_h, help_h, callback_h = make_handlers(config)
        
        app = Application.builder().token(token).build()
        app.add_handler(CommandHandler("start", start_h))
        app.add_handler(CommandHandler("plan", plan_h))
        app.add_handler(CommandHandler("help", help_h))
        app.add_handler(CallbackQueryHandler(callback_h))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_h))
        
        applications.append((bot_id, app))
        logger.info("bot_registered", bot_id=bot_id)
    
    logger.info("starting_all_bots", count=len(applications))
    
    # Initialize and start all bots
    tasks = []
    for bot_id, app in applications:
        await app.initialize()
        await app.start()
        # Start polling in background
        await app.updater.start_polling(drop_pending_updates=True)
        logger.info("bot_started", bot_id=bot_id)
    
    logger.info("all_bots_running", count=len(applications))
    
    # Keep running until interrupted
    try:
        stop_event = asyncio.Event()
        await stop_event.wait()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        for bot_id, app in applications:
            await app.updater.stop()
            await app.stop()
            await app.shutdown()
            logger.info("bot_stopped", bot_id=bot_id)


def main():
    """Entry point."""
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ]
    )
    asyncio.run(run_all_bots())


if __name__ == "__main__":
    main()
