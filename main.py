"""
MIRA AI Assistant
Main Application Entry Point

This file starts the complete MIRA assistant system.
"""

import sys
import asyncio
from pathlib import Path


# --------------------------------------------------
# PROJECT PATH SETUP
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


# --------------------------------------------------
# IMPORT MIRA SYSTEM
# --------------------------------------------------

from mira.core.assistant import MiraAssistant
from mira.utils.logger import setup_logger


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

async def main():

    logger = setup_logger()

    logger.info("=" * 60)
    logger.info("Starting MIRA AI Assistant")
    logger.info("=" * 60)

    try:

        # Create MIRA
        mira = MiraAssistant()

        # Initialize all systems
        await mira.initialize()

        print("\n" + "=" * 60)
        print("🤖 MIRA AI ASSISTANT IS READY")
        print("=" * 60)
        print("Type your message and press Enter.")
        print("Commands:")
        print("  exit   - Close MIRA")
        print("  quit   - Close MIRA")
        print("  help   - Show available commands")
        print("=" * 60 + "\n")

        # Start assistant
        await mira.run()

    except KeyboardInterrupt:

        print("\n\nMIRA: Goodbye! 👋")

    except Exception as error:

        logger.exception("MIRA crashed")

        print("\n❌ MIRA encountered an error:")
        print(error)

    finally:

        logger.info("MIRA shutting down")


# --------------------------------------------------
# PROGRAM START
# --------------------------------------------------

if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\nMIRA stopped.")
