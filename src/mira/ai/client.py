"""
MIRA AI Client.

Handles communication between MIRA and the configured AI provider.
"""

from __future__ import annotations

import asyncio
from typing import Any

from openai import AsyncOpenAI

from mira.ai.prompts import build_system_prompt
from mira.ai.providers import get_provider


class MiraAIClient:
    """
    Async AI client used by MIRA.
    """

    def __init__(
        self,
        config: dict[str, Any],
        api_key: str | None,
    ) -> None:

        self.config = config

        ai_config = config.get("ai", {})

        self.provider_name = ai_config.get(
            "provider",
            "openai",
        )

        self.timeout_seconds = ai_config.get(
            "timeout_seconds",
            60,
        )

        # Model can be configured using environment variable.
        self.model = (
            self._get_model_from_environment(ai_config)
        )

        self.api_key = api_key
        self.client: AsyncOpenAI | None = None

    async def initialize(self) -> None:
        """
        Initialize the configured AI provider.
        """

        get_provider(self.provider_name)

        if self.provider_name != "openai":
            raise RuntimeError(
                f"Provider not implemented: "
                f"{self.provider_name}"
            )

        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is missing. "
                "Configure it before starting MIRA."
            )

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            timeout=self.timeout_seconds,
        )

    async def generate_response(
        self,
        messages: list[dict[str, str]],
        route: str | None = None,
    ) -> str:
        """
        Generate a response from the AI model.
        """

        if self.client is None:
            raise RuntimeError(
                "AI client has not been initialized"
            )

        request_messages = [
            {
                "role": "system",
                "content": build_system_prompt(route),
            },
            *messages,
        ]

        try:
            response = await self.client.responses.create(
                model=self.model,
                input=request_messages,
            )

            text = response.output_text

            if not text or not text.strip():
                raise RuntimeError(
                    "AI provider returned an empty response"
                )

            return text.strip()

        except Exception as error:
            raise RuntimeError(
                f"AI request failed: {error}"
            ) from error

    async def close(self) -> None:
        """
        Close the AI client.

        The current OpenAI SDK does not always require explicit
        cleanup, but this method keeps MIRA's lifecycle consistent.
        """

        if self.client is not None:

            close_method = getattr(
                self.client,
                "close",
                None,
            )

            if close_method:

                result = close_method()

                if asyncio.iscoroutine(result):
                    await result

            self.client = None

    @staticmethod
    def _get_model_from_environment(
        ai_config: dict[str, Any],
    ) -> str:
        """
        Get model name from environment variables.

        Falls back to configuration if explicitly provided.
        """

        import os

        model_env = ai_config.get(
            "model_env",
            "MIRA_MODEL",
        )

        model = os.getenv(model_env)

        if model:
            return model

        configured_model = ai_config.get("model")

        if configured_model:
            return configured_model

        raise RuntimeError(
            "No AI model configured. "
            "Set MIRA_MODEL in your environment."
        )
