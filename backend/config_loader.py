from __future__ import annotations

import os
import signal
from pathlib import Path
from typing import Dict, Optional

import structlog
import yaml
from pydantic import BaseModel, Field, ValidationError

logger = structlog.get_logger(__name__)

BOTS_DIR = Path(os.getenv("BOTS_DIR", "./bots"))


class CountryConfig(BaseModel):
    code: str
    name: str
    language: str
    timezone: str
    currency: str


class NicheConfig(BaseModel):
    type: str
    category: str
    requires_disclaimer: bool = False
    disclaimer_type: Optional[str] = None


class LLMConfig(BaseModel):
    free_tier: str
    paid_tier: str
    fallback: str
    max_context_tokens: int = 4096
    temperature: float = 0.3
    knowledge_base: str = "knowledge/"


class PricingTier(BaseModel):
    price_usd: Optional[float] = None
    price_local: Optional[float] = None
    questions_per_day: Optional[int | str] = None
    features: list[str] = Field(default_factory=list)


class PricingConfig(BaseModel):
    free: PricingTier
    basic: PricingTier
    pro: PricingTier


class TelegramConfig(BaseModel):
    bot_token: Optional[str] = None
    bot_username: Optional[str] = None
    welcome_message: Optional[str] = None


class WebsiteConfig(BaseModel):
    domain: Optional[str] = None
    template: Optional[str] = None
    primary_color: Optional[str] = None
    logo: Optional[str] = None


class FaqItem(BaseModel):
    question: str
    answer: str


class BotConfig(BaseModel):
    bot_id: str
    name: str
    tagline: str
    country: CountryConfig
    niche: NicheConfig
    llm: LLMConfig
    pricing: PricingConfig
    payment: dict
    telegram: Optional[TelegramConfig] = None
    website: Optional[WebsiteConfig] = None
    seo: Optional[dict] = None
    marketing: Optional[dict] = None

    system_prompt: Optional[str] = None
    disclaimer: Optional[str] = None
    faq: list[FaqItem] = Field(default_factory=list)


_CONFIG_CACHE: Dict[str, BotConfig] = {}


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_text(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def _expand_env(value: object) -> object:
    if isinstance(value, str) and "${" in value:
        for key, env_val in os.environ.items():
            value = value.replace(f"${{{key}}}", env_val)
        return value
    if isinstance(value, list):
        return [_expand_env(v) for v in value]
    if isinstance(value, dict):
        return {k: _expand_env(v) for k, v in value.items()}
    return value


def load_all_configs() -> Dict[str, BotConfig]:
    configs: Dict[str, BotConfig] = {}
    if not BOTS_DIR.exists():
        logger.warning("bots_dir_missing", path=str(BOTS_DIR))
        return configs

    for config_path in BOTS_DIR.rglob("config.yaml"):
        try:
            raw = _load_yaml(config_path)
            raw = _expand_env(raw)
            bot_dir = config_path.parent
            system_prompt = _load_text(bot_dir / "system_prompt.md")
            disclaimer = _load_text(bot_dir / "disclaimer.md")
            raw["system_prompt"] = system_prompt
            raw["disclaimer"] = disclaimer
            # Load FAQ
            faq_path = bot_dir / "faq.yaml"
            if faq_path.exists():
                try:
                    faq_raw = yaml.safe_load(faq_path.read_text(encoding="utf-8")) or []
                    raw["faq"] = faq_raw if isinstance(faq_raw, list) else []
                except Exception:  # noqa: BLE001
                    raw["faq"] = []
            config = BotConfig(**raw)
            configs[config.bot_id] = config
        except (ValidationError, yaml.YAMLError) as exc:
            logger.error("config_load_failed", path=str(config_path), error=str(exc))
        except Exception as exc:  # noqa: BLE001
            logger.exception("config_load_unexpected", path=str(config_path), error=str(exc))

    logger.info("configs_loaded", count=len(configs))
    return configs


def reload_configs() -> None:
    global _CONFIG_CACHE
    _CONFIG_CACHE = load_all_configs()


def get_bot_config(bot_id: str) -> Optional[BotConfig]:
    return _CONFIG_CACHE.get(bot_id)


def get_all_configs() -> Dict[str, BotConfig]:
    return _CONFIG_CACHE


def setup_signal_handlers() -> None:
    try:
        signal.signal(signal.SIGHUP, lambda *_: reload_configs())
    except Exception as exc:  # noqa: BLE001
        logger.warning("signal_setup_failed", error=str(exc))


# Initial load at import
reload_configs()
setup_signal_handlers()
