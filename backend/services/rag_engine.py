from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Dict, List

import faiss
import structlog
from sentence_transformers import SentenceTransformer

from backend.config_loader import BotConfig

logger = structlog.get_logger(__name__)

_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_CHUNK_WORDS = 500


class RAGIndex:
    def __init__(self, index: faiss.Index, chunks: List[str]):
        self.index = index
        self.chunks = chunks


class RAGEngine:
    def __init__(self) -> None:
        self._model = SentenceTransformer(_MODEL_NAME)
        self._indexes: Dict[str, RAGIndex] = {}

    def _chunk_text(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), _CHUNK_WORDS):
            chunk = " ".join(words[i : i + _CHUNK_WORDS]).strip()
            if chunk:
                chunks.append(chunk)
        return chunks

    def _load_files(self, knowledge_dir: Path) -> List[str]:
        contents: List[str] = []
        if not knowledge_dir.exists():
            return contents
        for path in knowledge_dir.rglob("*"):
            if path.is_dir():
                continue
            if path.suffix.lower() not in {".md", ".txt", ".yaml", ".yml"}:
                continue
            try:
                contents.append(path.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                logger.warning("rag_file_read_failed", path=str(path), error=str(exc))
        return contents

    def _build_index(self, texts: List[str]) -> RAGIndex:
        chunks: List[str] = []
        for text in texts:
            chunks.extend(self._chunk_text(text))
        if not chunks:
            index = faiss.IndexFlatL2(384)
            return RAGIndex(index, [])

        embeddings = self._model.encode(chunks, convert_to_numpy=True, show_progress_bar=False)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return RAGIndex(index, chunks)

    async def initialize_bot(self, bot_id: str, bot_dir: Path, config: BotConfig) -> None:
        knowledge_path = bot_dir / config.llm.knowledge_base
        texts = await asyncio.to_thread(self._load_files, knowledge_path)
        rag_index = await asyncio.to_thread(self._build_index, texts)
        self._indexes[bot_id] = rag_index
        logger.info("rag_index_ready", bot_id=bot_id, chunks=len(rag_index.chunks))

    async def initialize(self, bot_configs: Dict[str, BotConfig], bots_dir: Path) -> None:
        tasks = []
        for bot_id, config in bot_configs.items():
            bot_dir = bots_dir / bot_id
            tasks.append(self.initialize_bot(bot_id, bot_dir, config))
        if tasks:
            await asyncio.gather(*tasks)

    async def get_relevant_chunks(self, bot_id: str, query: str, top_k: int = 3) -> List[str]:
        rag_index = self._indexes.get(bot_id)
        if not rag_index or not rag_index.chunks:
            return []
        query_embedding = await asyncio.to_thread(
            self._model.encode, [query], convert_to_numpy=True, show_progress_bar=False
        )
        distances, indices = rag_index.index.search(query_embedding, top_k)
        results: List[str] = []
        for idx in indices[0]:
            if 0 <= idx < len(rag_index.chunks):
                results.append(rag_index.chunks[idx])
        return results


rag_engine = RAGEngine()
