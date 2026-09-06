"""
Conversation context management.

This module keeps the recent conversation history in memory.
Long-term memory will later be handled by the memory package.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Message:
    role: str
    content: str
    created_at: datetime


class ConversationContext:
    """
    Stores recent conversation messages.
    """

    VALID_ROLES = {"system", "user", "assistant"}

    def __init__(self, max_messages: int = 20) -> None:
        if max_messages < 2:
            raise ValueError("max_messages must be at least 2")

        self.max_messages = max_messages
        self._messages: list[Message] = []

    def add(self, role: str, content: str) -> None:
        role = role.strip().lower()
        content = content.strip()

        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role: {role}")

        if not content:
            return

        self._messages.append(
            Message(
                role=role,
                content=content,
                created_at=datetime.now(timezone.utc),
            )
        )

        self._trim()

    def add_user(self, content: str) -> None:
        self.add("user", content)

    def add_assistant(self, content: str) -> None:
        self.add("assistant", content)

    def add_system(self, content: str) -> None:
        self.add("system", content)

    def get_messages(self) -> list[dict[str, str]]:
        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in self._messages
        ]

    def get_recent(self, limit: int | None = None) -> list[dict[str, str]]:
        messages = self.get_messages()

        if limit is None:
            return messages

        return messages[-limit:]

    def clear(self) -> None:
        self._messages.clear()

    def _trim(self) -> None:
        system_messages = [
            message
            for message in self._messages
            if message.role == "system"
        ]

        non_system_messages = [
            message
            for message in self._messages
            if message.role != "system"
        ]

        non_system_limit = max(
            self.max_messages - len(system_messages),
            0,
        )

        non_system_messages = non_system_messages[-non_system_limit:]

        self._messages = system_messages + non_system_messages
