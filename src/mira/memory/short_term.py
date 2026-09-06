"""
Short-term memory for the current MIRA session.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class ShortTermMemoryItem:
    content: str
    created_at: datetime


class ShortTermMemory:
    def __init__(
        self,
        limit: int = 20,
    ) -> None:

        self.limit = limit

        self._items = deque(
            maxlen=limit
        )

    def add(
        self,
        content: str,
    ) -> None:

        content = content.strip()

        if not content:
            return

        self._items.append(
            ShortTermMemoryItem(
                content=content,
                created_at=datetime.now(
                    timezone.utc
                ),
            )
        )

    def get_all(self) -> list[str]:
        return [
            item.content
            for item in self._items
        ]

    def get_recent(
        self,
        limit: int = 5,
    ) -> list[str]:

        items = list(self._items)

        return [
            item.content
            for item in items[-limit:]
        ]

    def clear(self) -> None:
        self._items.clear()
