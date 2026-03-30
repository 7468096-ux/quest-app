# SmartHelp — AI Bots Platform

Config-driven platform for multi-country, multi-niche AI bots (Telegram + web) powered by a shared FastAPI backend.

## Quick Start

```bash
cd projects/ai-bots-platform
cp .env.example .env
# edit .env with your keys

# run locally (requires Docker)
docker compose up -d --build
```

API:
- `POST /api/auth/telegram`
- `POST /api/auth/web`
- `POST /api/chat`

## Create a New Bot

```bash
python scripts/create_bot.py --country BR --niche tutor --name TutorIA --language pt-BR
```

This creates a new folder under `bots/<country>-<niche>/` with `config.yaml`, `system_prompt.md`, and `disclaimer.md`.

## Development

- Backend code lives in `backend/`
- Bot configurations live in `bots/`
- RAG indexes are created on startup from `knowledge/`

## Migrations

```bash
cd backend
alembic upgrade head
```
