"""
MIRA AI Assistant package.

This package contains the core systems used by the MIRA
Windows AI Assistant.
"""

from importlib.metadata import PackageNotFoundError, version


try:
    __version__ = version("mira-ai-assistant")
except PackageNotFoundError:
    # Development mode: package may not be installed yet.
    __version__ = "1.0.0"


__app_name__ = "MIRA"
__description__ = "Ultra Advanced Personal AI Assistant"


def get_app_info() -> dict[str, str]:
    """
    Return basic application metadata.
    """
    return {
        "name": __app_name__,
        "version": __version__,
        "description": __description__,
    }
