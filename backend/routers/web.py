"""Web router — serves config-driven landing pages for all bots.

Routes:
  GET /              → list all bots (index page)
  GET /{cc}/{niche}  → landing page for a specific bot (e.g. /br/lawyer)
  GET /bots          → JSON list of all bots (for frontend enumeration)
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import structlog
import yaml
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.config_loader import get_all_configs, BotConfig

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["web"])

# Paths — resolve relative to this file's location
_WEB_DIR = Path(__file__).resolve().parents[2] / "web"
templates = Jinja2Templates(directory=str(_WEB_DIR / "templates"))
_TRANS_DIR = _WEB_DIR / "translations"

# Language → translations dict (loaded once)
_translations: dict[str, dict] = {}

def _load_translations() -> dict[str, dict]:
    trans: dict[str, dict] = {}
    if not _TRANS_DIR.exists():
        return trans
    for f in _TRANS_DIR.glob("*.yaml"):
        lang = f.stem  # e.g. "pt-BR", "ru", "en"
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            trans[lang] = data
        except Exception as exc:  # noqa: BLE001
            logger.warning("translation_load_failed", file=str(f), error=str(exc))
    return trans


def _get_translations(language: str) -> dict:
    """Return translations for a language, falling back to 'en'."""
    if not _translations:
        _translations.update(_load_translations())
    return _translations.get(language) or _translations.get("en") or {}


# Niche → emoji mapping
NICHE_EMOJI: dict[str, str] = {
    "lawyer": "⚖️",
    "tutor": "📚",
    "accountant": "💰",
    "doctor": "🏥",
    "realtor": "🏠",
    "agronomist": "🌾",
    "sales": "🛒",
    "translator": "🎓",
}


def _find_bot_by_country_niche(country_code: str, niche_type: str) -> Optional[BotConfig]:
    """Find a bot config by country code and niche type."""
    configs = get_all_configs()
    cc = country_code.lower()
    niche = niche_type.lower()
    # First try exact bot_id match: "{cc}-{niche}"
    exact_id = f"{cc}-{niche}"
    if exact_id in configs:
        return configs[exact_id]
    # Fallback: search by country code + niche type
    for config in configs.values():
        if (
            config.country.code.lower() == cc
            and config.niche.type.lower() == niche
        ):
            return config
    return None


@router.get("/bots", response_class=HTMLResponse)
async def list_bots_page(request: Request) -> HTMLResponse:
    """Simple index listing all available bots."""
    configs = get_all_configs()
    bot_list = sorted(configs.values(), key=lambda c: (c.country.code, c.niche.type))

    rows = []
    for c in bot_list:
        emoji = NICHE_EMOJI.get(c.niche.type.lower(), "🤖")
        rows.append(
            f'<tr>'
            f'<td>{emoji} {c.name}</td>'
            f'<td>{c.country.code}</td>'
            f'<td>{c.niche.type}</td>'
            f'<td><a href="/{c.country.code.lower()}/{c.niche.type.lower()}">Open</a></td>'
            f'</tr>'
        )

    html = f"""<!DOCTYPE html>
<html><head><title>SmartHelp — All Bots</title>
<style>body{{font-family:sans-serif;max-width:800px;margin:40px auto;padding:0 20px}}
table{{width:100%;border-collapse:collapse}}th,td{{padding:8px 12px;border:1px solid #ddd;text-align:left}}
th{{background:#f5f5f5}}a{{color:#2563eb}}</style></head>
<body><h1>🤖 SmartHelp — Available Bots ({len(bot_list)})</h1>
<table><tr><th>Bot</th><th>Country</th><th>Niche</th><th>Link</th></tr>
{"".join(rows)}
</table></body></html>"""
    return HTMLResponse(html)


@router.get("/{country_code}/{niche_type}", response_class=HTMLResponse)
async def landing_page(
    request: Request,
    country_code: str,
    niche_type: str,
) -> HTMLResponse:
    """Serve the config-driven landing page for a specific bot."""
    config = _find_bot_by_country_niche(country_code, niche_type)
    if not config:
        raise HTTPException(
            status_code=404,
            detail=f"Bot not found: {country_code}/{niche_type}",
        )

    translations = _get_translations(config.country.language)
    niche_emoji = NICHE_EMOJI.get(config.niche.type.lower(), "🤖")
    disclaimer_text = config.disclaimer or ""

    return templates.TemplateResponse(
        "landing.html",
        {
            "request": request,
            "config": config,
            "translations": translations,
            "niche_emoji": niche_emoji,
            "disclaimer_text": disclaimer_text,
        },
    )
