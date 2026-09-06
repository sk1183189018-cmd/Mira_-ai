"""
Main MIRA Assistant runtime.

This is the central application controller.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

from mira.ai.client import MiraAIClient
from mira.core.brain import MiraBrain
from mira.core.context import ConversationContext
from mira.core.planner import TaskPlanner
from mira.core.router import CommandRouter
from mira.core.state import (
    AssistantStatus,
    StateManager,
)
from mira.utils.logger import get_logger


class MiraAssistant:
    """
    Main runtime controller for the MIRA AI Assistant.
    """

    def __init__(self) -> None:
        self.project_root = (
            Path(__file__).resolve().parents[3]
        )

        self.config: dict = {}
        self.logger = get_logger("mira.assistant")

        self.state = StateManager()

        self.ai_client = None
        self.context = None
        self.router = None
        self.planner = None
        self.brain = None

        self.running = False

    async def initialize(self) -> None:
        """
        Initialize all core MIRA systems.
        """

        self.state.set_status(AssistantStatus.STARTING)

        load_dotenv(
            self.project_root / ".env"
        )

        self.config = self._load_config()

        self._ensure_directories()

        max_history = (
            self.config
            .get("conversation", {})
            .get("max_context_messages", 20)
        )

        self.context = ConversationContext(
            max_messages=max_history
        )

        self.router = CommandRouter()

        self.planner = TaskPlanner()

        self.ai_client = MiraAIClient(
            config=self.config,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        await self.ai_client.initialize()

        self.brain = MiraBrain(
            ai_client=self.ai_client,
            context=self.context,
            router=self.router,
            planner=self.planner,
        )

        self.state.set_status(AssistantStatus.READY)

        self.logger.info(
            "MIRA initialized successfully"
        )

    async def run(self) -> None:
        """
        Start the MIRA command loop.

        This terminal loop is useful during development.
        The final Windows GUI will call process_message()
        directly and users will not need a terminal.
        """

        if self.brain is None:
            raise RuntimeError(
                "MIRA has not been initialized"
            )

        self.running = True

        while self.running:
            try:
                user_input = await asyncio.to_thread(
                    input,
                    "You: ",
                )

                user_input = user_input.strip()

                if not user_input:
                    continue

                result = await self.process_message(
                    user_input
                )

                print(f"\nMIRA: {result['response']}\n")

                if result["type"] == "exit":
                    await self.shutdown()

            except EOFError:
                await self.shutdown()

            except KeyboardInterrupt:
                await self.shutdown()

            except Exception as error:
                self.state.set_error(error)

                self.logger.exception(
                    "Error while processing user request"
                )

                print(
                    "\nMIRA: Sorry, something went wrong."
                )

    async def process_message(
        self,
        message: str,
    ) -> dict:
        """
        Process one message.

        This method will be used by:
        - GUI
        - voice system
        - terminal development mode
        """

        if not self.brain:
            raise RuntimeError(
                "MIRA Brain is not initialized"
            )

        self.state.clear_error()
        self.state.set_status(
            AssistantStatus.THINKING
        )
        self.state.set_current_task(message)

        try:
            result = await self.brain.process(message)

            self.state.set_current_task(None)
            self.state.set_status(
                AssistantStatus.READY
            )

            return result

        except Exception as error:
            self.state.set_error(error)
            raise

    async def shutdown(self) -> None:
        """
        Safely shut down MIRA.
        """

        if not self.running:
            return

        self.state.set_status(
            AssistantStatus.STOPPING
        )

        self.running = False

        if self.ai_client:
            await self.ai_client.close()

        self.state.set_status(
            AssistantStatus.STOPPED
        )

        self.logger.info(
            "MIRA shutdown completed"
        )

    def _load_config(self) -> dict:
        config_file = (
            self.project_root
            / "config"
            / "settings.yaml"
        )

        if not config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found: "
                f"{config_file}"
            )

        with config_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            config = yaml.safe_load(file)

        return config or {}

    def _ensure_directories(self) -> None:
        directories = [
            self.project_root / "logs",
            self.project_root / "data",
            self.project_root / "data" / "screenshots",
            self.project_root / "data" / "projects",
        ]

        for directory in directories:
            directory.mkdir(
                parents=True,
                exist_ok=True,
                  )
