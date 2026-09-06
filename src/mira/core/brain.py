"""
MIRA Brain.

The brain coordinates:
- conversation context
- command routing
- task planning
- AI responses
"""

from __future__ import annotations

from mira.core.context import ConversationContext
from mira.core.planner import TaskPlanner
from mira.core.router import CommandRouter, Route


class MiraBrain:
    """
    Central reasoning coordinator for MIRA.
    """

    def __init__(
        self,
        ai_client,
        context: ConversationContext,
        router: CommandRouter,
        planner: TaskPlanner,
    ) -> None:
        self.ai_client = ai_client
        self.context = context
        self.router = router
        self.planner = planner

    async def process(self, user_message: str) -> dict:
        """
        Process a user request and return structured information.
        """

        route_result = self.router.route(user_message)

        if route_result.route == Route.EXIT:
            return {
                "type": "exit",
                "response": "Goodbye! MIRA is shutting down.",
                "route": route_result.route.value,
            }

        if route_result.route == Route.HELP:
            return {
                "type": "help",
                "response": self._help_message(),
                "route": route_result.route.value,
            }

        self.context.add_user(user_message)

        plan = self.planner.create_plan(
            goal=user_message,
            route=route_result.route.value,
        )

        # Specialist agents will be connected later.
        # For now, the real AI client handles the request
        # while preserving the route and conversation context.
        response = await self.ai_client.generate_response(
            messages=self.context.get_messages(),
            route=route_result.route.value,
        )

        self.context.add_assistant(response)

        return {
            "type": "response",
            "response": response,
            "route": route_result.route.value,
            "plan_id": plan.id,
        }

    @staticmethod
    def _help_message() -> str:
        return (
            "I am MIRA. I can help with conversation, coding, "
            "computer tasks, files, web research, screenshots, "
            "and automation as these modules are enabled."
        )
