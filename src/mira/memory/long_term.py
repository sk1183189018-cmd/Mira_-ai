"""
Long-term persistent memory for MIRA.
"""

from __future__ import annotations

from mira.memory.database import MemoryDatabase


class LongTermMemory:
    def __init__(
        self,
        database: MemoryDatabase,
    ) -> None:

        self.database = database

    def remember(
        self,
        content: str,
        category: str = "general",
        importance: int = 1,
    ) -> int:

        content = content.strip()

        if not content:
            raise ValueError(
                "Memory content cannot be empty"
            )

        importance = max(
            1,
            min(importance, 10),
        )

        return self.database.add_memory(
            category=category,
            content=content,
            importance=importance,
        )

    def search(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict]:

        return self.database.search_memories(
            query=query,
            limit=limit,
        )

    def recent(
        self,
        limit: int = 20,
    ) -> list[dict]:

        return self.database.get_recent(
            limit=limit
        )

    def forget(
        self,
        memory_id: int,
    ) -> bool:

        return self.database.delete_memory(
            memory_id
        )

    def clear(self) -> None:
        self.database.clear_all()
