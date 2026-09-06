"""
Application state management for MIRA.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from threading import RLock
from typing import Any


class AssistantStatus(str, Enum):
    STARTING = "starting"
    READY = "ready"
    THINKING = "thinking"
    EXECUTING = "executing"
    SPEAKING = "speaking"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class AssistantState:
    status: AssistantStatus = AssistantStatus.STARTING
    current_task: str | None = None
    last_error: str | None = None
    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, Any] = field(default_factory=dict)


class StateManager:
    """
    Thread-safe manager for MIRA's runtime state.
    """

    def __init__(self) -> None:
        self._state = AssistantState()
        self._lock = RLock()

    def get_state(self) -> AssistantState:
        with self._lock:
            return AssistantState(
                status=self._state.status,
                current_task=self._state.current_task,
                last_error=self._state.last_error,
                started_at=self._state.started_at,
                updated_at=self._state.updated_at,
                metadata=dict(self._state.metadata),
            )

    def set_status(self, status: AssistantStatus) -> None:
        with self._lock:
            self._state.status = status
            self._state.updated_at = datetime.now(timezone.utc)

    def set_current_task(self, task: str | None) -> None:
        with self._lock:
            self._state.current_task = task
            self._state.updated_at = datetime.now(timezone.utc)

    def set_error(self, error: Exception | str) -> None:
        with self._lock:
            self._state.last_error = str(error)
            self._state.status = AssistantStatus.ERROR
            self._state.updated_at = datetime.now(timezone.utc)

    def update_metadata(self, **values: Any) -> None:
        with self._lock:
            self._state.metadata.update(values)
            self._state.updated_at = datetime.now(timezone.utc)

    def clear_error(self) -> None:
        with self._lock:
            self._state.last_error = None
            self._state.updated_at = datetime.now(timezone.utc)
