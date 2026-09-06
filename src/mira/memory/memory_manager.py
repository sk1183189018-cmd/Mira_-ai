"""
Main Memory Manager for MIRA.
"""

from __future__ import annotations

from mira.memory.database import MemoryDatabase
from mira.memory.long_term import LongTermMemory
from mira.memory.short_term import ShortTermMemory


class MemoryManager:
    """
    Coordinates short-term and long-term memory.
    """

    def __init__(
        self,
        database_path: str,
        short_term_limit: int = 20,
        long_term_enabled: bool = True,
    ) -> None:

        self.short_term = ShortTermMemory(
            limit=short_term_limit
        )

        self.long_term_enabled = (
            long_term_enabled
        )

        self.database = MemoryDatabase(
            database_path
        )

        self.long_term = LongTermMemory(
            self.database
        )

    def add_conversation(
        self,
        role: str,
        content: str,
    ) -> None:

        self.short_term.add(
            f"{role}: {content}"
        )

    def remember(
        self,
        content: str,
        category: str = "general",
        importance: int = 1,
    ) -> int | None:

        if not self.long_term_enabled:
            return None

        return self.long_term.remember(
            content=content,
            category=category,
            importance=importance,
        )

    def recall(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:

        if not self.long_term_enabled:
            return []

        return self.long_term.search(
            query=query,
            limit=limit,
        )

    def get_context(self) -> dict:

        return {
            "short_term": (
                self.short_term.get_recent(10)
            ),
            "long_term": (
                self.long_term.recent(10)
                if self.long_term_enabled
                else []
            ),
        }

    def forget(
        self,
        memory_id: int,
    ) -> bool:

        return self.long_term.forget(
            memory_id
        )

    def clear_session(self) -> None:

        self.short_term.clear()
