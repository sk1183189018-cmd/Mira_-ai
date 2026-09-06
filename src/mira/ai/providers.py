"""
AI provider definitions.

This module keeps provider-specific configuration separate
from the rest of MIRA.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProviderConfig:
    name: str
    enabled: bool = True


SUPPORTED_PROVIDERS = {
    "openai": ProviderConfig(
        name="openai",
        enabled=True,
    ),
}


def get_provider(name: str) -> ProviderConfig:
    """
    Return provider configuration.
    """

    provider_name = name.strip().lower()

    if provider_name not in SUPPORTED_PROVIDERS:
        supported = ", ".join(SUPPORTED_PROVIDERS)

        raise ValueError(
            f"Unsupported AI provider: {name}. "
            f"Supported providers: {supported}"
        )

    return SUPPORTED_PROVIDERS[provider_name]
