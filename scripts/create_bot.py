from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import structlog
import yaml

logger = structlog.get_logger(__name__)

ROOT = Path(__file__).resolve().parents[1]
BOTS_DIR = ROOT / "bots"


def make_bot_id(country: str, niche: str) -> str:
    return f"{country.lower()}-{niche.lower()}"


def bot_token_env_var(bot_id: str) -> str:
    return f"{bot_id.replace('-', '_').upper()}_BOT_TOKEN"


def system_prompt_template(name: str, niche: str, country: str, language: str, disclaimer: str) -> str:
    return f"""# System Prompt: {name}

## Role
Você é um assistente especializado em {niche} para usuários de {country}.
Você se comunica em {language}.

## Rules
1. Responda apenas perguntas relacionadas ao tema {niche}.
2. Se a pergunta estiver fora do tema, recuse educadamente.
3. Use o contexto da base de conhecimento quando disponível.
4. Se não tiver certeza, diga isso e recomende consultar um especialista.
5. Sempre inclua o aviso legal ao final da resposta.
6. Seja claro, conciso e estruturado.

## Disclaimer
{disclaimer}

## Knowledge Base Context
{{rag_chunks}}
"""


def default_disclaimer(niche: str) -> str:
    if niche.lower() == "lawyer":
        return "⚖️ Aviso: Sou uma IA informativa. Minhas respostas NÃO constituem aconselhamento jurídico profissional."
    if niche.lower() == "doctor":
        return "🏥 Aviso: Sou uma IA informativa sobre saúde. NÃO substituo consulta médica."
    if niche.lower() == "accountant":
        return "💰 Aviso: Informações gerais sobre impostos. Para declarações fiscais, consulte um contador registrado."
    return "ℹ️ Aviso: Sou uma IA informativa. Minhas respostas não substituem profissionais especializados."


def create_bot(
    country: str,
    niche: str,
    name: str,
    language: str,
    price_basic: Optional[float],
    price_pro: Optional[float],
) -> Path:
    bot_id = make_bot_id(country, niche)
    bot_dir = BOTS_DIR / bot_id
    bot_dir.mkdir(parents=True, exist_ok=True)

    disclaimer = default_disclaimer(niche)
    config = {
        "bot_id": bot_id,
        "name": name,
        "tagline": f"Assistente {niche} com IA",
        "country": {
            "code": country.upper(),
            "name": country.upper(),
            "language": language,
            "timezone": "UTC",
            "currency": "USD",
        },
        "niche": {
            "type": niche,
            "category": niche,
            "requires_disclaimer": True,
            "disclaimer_type": "default",
        },
        "llm": {
            "free_tier": "gemini-2.0-flash",
            "paid_tier": "gpt-4o-mini",
            "fallback": "ollama/llama3.2:3b",
            "max_context_tokens": 4096,
            "temperature": 0.5,
            "knowledge_base": "knowledge/",
        },
        "pricing": {
            "free": {"questions_per_day": 3, "features": ["basic_answers"]},
            "basic": {
                "price_usd": price_basic or 9,
                "price_local": price_basic or 9,
                "questions_per_day": 30,
                "features": ["basic_answers", "chat_history"],
            },
            "pro": {
                "price_usd": price_pro or 19,
                "price_local": price_pro or 19,
                "questions_per_day": "unlimited",
                "features": ["all"],
            },
        },
        "payment": {"stripe": True, "local_providers": [], "telegram_stars": True},
        "telegram": {
            "bot_token": f"${{{bot_token_env_var(bot_id)}}}",
            "bot_username": "",
            "welcome_message": (
                f"Olá! Eu sou {name}.\n"
                f"Posso ajudar com dúvidas sobre {niche}.\n\n"
                "⚠️ Importante: sou uma IA e não substituo um especialista."
            ),
        },
        "website": {
            "domain": f"{bot_id}.smarthelp.ai",
            "template": "chat-landing",
            "primary_color": "#1a5276",
            "logo": "assets/logo.svg",
        },
        "seo": {
            "title": f"{name} — Assistente {niche} com IA",
            "description": f"Assistente {niche} com IA para {country.upper()}.",
            "keywords": [f"{niche} ia", f"{country.lower()} {niche}", "smarthelp"],
        },
        "marketing": {"target_groups": [], "launch_offer": ""},
    }

    knowledge_dir = bot_dir / "knowledge"
    knowledge_dir.mkdir(exist_ok=True)

    (knowledge_dir / "README.md").write_text(
        "# Knowledge Base\n\n" "Adicione arquivos .md com conteúdo relevante para o bot.\n",
        encoding="utf-8",
    )

    (bot_dir / "faq.yaml").write_text("[]\n", encoding="utf-8")

    with (bot_dir / "config.yaml").open("w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, sort_keys=False, allow_unicode=True)

    (bot_dir / "system_prompt.md").write_text(
        system_prompt_template(name, niche, country, language, disclaimer),
        encoding="utf-8",
    )
    (bot_dir / "disclaimer.md").write_text(disclaimer, encoding="utf-8")

    logger.info("bot_created", bot_id=bot_id, path=str(bot_dir))
    return bot_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a new bot configuration")
    parser.add_argument("--country", required=True)
    parser.add_argument("--niche", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--language", required=True)
    parser.add_argument("--price-basic", type=float, default=None)
    parser.add_argument("--price-pro", type=float, default=None)

    args = parser.parse_args()
    create_bot(args.country, args.niche, args.name, args.language, args.price_basic, args.price_pro)


if __name__ == "__main__":
    main()
