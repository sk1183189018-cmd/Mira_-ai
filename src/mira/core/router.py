"""
Command routing for MIRA.

The router detects whether a user request should be handled
by a specialist system or by the main AI conversation system.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Route(str, Enum):
    CHAT = "chat"
    COMPUTER = "computer"
    FILES = "files"
    WEB = "web"
    CODING = "coding"
    VISION = "vision"
    AUTOMATION = "automation"
    HELP = "help"
    EXIT = "exit"


@dataclass
class RouteResult:
    route: Route
    confidence: float
    reason: str


class CommandRouter:
    """
    Rule-based first-level router.

    AI-based routing can later be added on top of this system.
    """

    def route(self, command: str) -> RouteResult:
        text = command.strip().lower()

        if not text:
            return RouteResult(
                route=Route.CHAT,
                confidence=0.0,
                reason="Empty input",
            )

        if text in {"exit", "quit", "bye", "stop mira"}:
            return RouteResult(
                Route.EXIT,
                1.0,
                "User requested shutdown",
            )

        if text in {"help", "commands", "what can you do"}:
            return RouteResult(
                Route.HELP,
                1.0,
                "User requested help",
            )

        if any(
            word in text
            for word in (
                "open ",
                "close ",
                "volume",
                "screenshot",
                "running app",
                "application",
            )
        ):
            return RouteResult(
                Route.COMPUTER,
                0.85,
                "Computer-related command detected",
            )

        if any(
            word in text
            for word in (
                "file",
                "folder",
                "rename",
                "move file",
                "delete file",
                "find my",
            )
        ):
            return RouteResult(
                Route.FILES,
                0.85,
                "File-related command detected",
            )

        if any(
            word in text
            for word in (
                "search web",
                "search online",
                "research",
                "latest news",
                "google",
            )
        ):
            return RouteResult(
                Route.WEB,
                0.85,
                "Web-related command detected",
            )

        if any(
            word in text
            for word in (
                "python code",
                "write code",
                "debug",
                "bug",
                "error in code",
                "create project",
                "programming",
            )
        ):
            return RouteResult(
                Route.CODING,
                0.85,
                "Coding-related command detected",
            )

        if any(
            word in text
            for word in (
                "look at screen",
                "analyze screenshot",
                "read screen",
                "screen error",
            )
        ):
            return RouteResult(
                Route.VISION,
                0.85,
                "Vision-related command detected",
            )

        if any(
            word in text
            for word in (
                "automate",
                "schedule",
                "workflow",
                "every day",
            )
        ):
            return RouteResult(
                Route.AUTOMATION,
                0.85,
                "Automation-related command detected",
            )

        return RouteResult(
            Route.CHAT,
            0.60,
            "General conversation",
          )
