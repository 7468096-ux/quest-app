from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, Tuple

import httpx
import structlog
from google import generativeai as genai
from openai import AsyncOpenAI

from backend.config_loader import BotConfig

logger = structlog.get_logger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

_openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def build_prompt(system_prompt: str, rag_chunks: list[str], history: list[dict], user_message: str) -> str:
    sections = [system_prompt or ""]
    if rag_chunks:
        sections.append("\n\n# Knowledge Base Context\n" + "\n\n".join(rag_chunks))
    if history:
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])
        sections.append("\n\n# Conversation History\n" + history_text)
    sections.append(f"\n\n# User\n{user_message}")
    return "\n".join(sections).strip()


async def _call_gemini(prompt: str, model: str, temperature: float) -> Tuple[str, Dict[str, Any]]:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")

    def _run() -> Any:
        gemini_model = genai.GenerativeModel(model)
        return gemini_model.generate_content(prompt, generation_config={"temperature": temperature})

    response = await asyncio.to_thread(_run)
    text = response.text
    usage = {
        "prompt_tokens": getattr(response, "prompt_token_count", 0) or 0,
        "completion_tokens": getattr(response, "candidates_token_count", 0) or 0,
        "model": model,
    }
    return text, usage


async def _call_openai(prompt: str, model: str, temperature: float) -> Tuple[str, Dict[str, Any]]:
    if not _openai_client:
        raise RuntimeError("OPENAI_API_KEY not set")
    response = await _openai_client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[{"role": "system", "content": ""}, {"role": "user", "content": prompt}],
    )
    text = response.choices[0].message.content or ""
    usage = {
        "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
        "completion_tokens": response.usage.completion_tokens if response.usage else 0,
        "model": model,
    }
    return text, usage


async def _call_ollama(prompt: str, model: str, temperature: float) -> Tuple[str, Dict[str, Any]]:
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model.split("/", 1)[-1], "prompt": prompt, "stream": False, "temperature": temperature},
        )
        resp.raise_for_status()
        data = resp.json()
        text = data.get("response", "")
        usage = {
            "prompt_tokens": data.get("prompt_eval_count", 0),
            "completion_tokens": data.get("eval_count", 0),
            "model": model,
        }
        return text, usage


async def route_llm(
    config: BotConfig,
    subscription_plan: str,
    rag_chunks: list[str],
    history: list[dict],
    user_message: str,
) -> Tuple[str, Dict[str, Any]]:
    prompt = build_prompt(config.system_prompt or "", rag_chunks, history, user_message)
    model_primary = config.llm.free_tier if subscription_plan == "free" else config.llm.paid_tier
    temperature = config.llm.temperature

    try:
        if subscription_plan == "free":
            return await _call_gemini(prompt, model_primary, temperature)
        return await _call_openai(prompt, model_primary, temperature)
    except Exception as exc:  # noqa: BLE001
        logger.warning("primary_llm_failed", error=str(exc), model=model_primary)
        try:
            return await _call_ollama(prompt, config.llm.fallback, temperature)
        except Exception as fallback_exc:  # noqa: BLE001
            logger.error("fallback_llm_failed", error=str(fallback_exc))
            raise
