"""
Data models used by the MIRA AI system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AIMessage:
    role: str
    content: str


@dataclass(slots=True)
class AIResponse:
    content: str
    model: str
    usage: dict[str, Any] = field(default_factory=dict)
    raw: Any | None = None
