"""
Task planning system for MIRA.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskStep:
    id: str
    description: str
    action: str
    status: StepStatus = StepStatus.PENDING
    result: str | None = None


@dataclass
class TaskPlan:
    id: str
    goal: str
    steps: list[TaskStep] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return bool(self.steps) and all(
            step.status == StepStatus.COMPLETED
            for step in self.steps
        )


class TaskPlanner:
    """
    Creates simple executable plans.

    The AI Brain can later generate more advanced plans.
    """

    def create_plan(
        self,
        goal: str,
        route: str,
    ) -> TaskPlan:
        plan = TaskPlan(
            id=str(uuid4()),
            goal=goal,
        )

        plan.steps.append(
            TaskStep(
                id=str(uuid4()),
                description="Understand the user request",
                action="analyze",
            )
        )

        plan.steps.append(
            TaskStep(
                id=str(uuid4()),
                description=f"Send task to {route} system",
                action=route,
            )
        )

        plan.steps.append(
            TaskStep(
                id=str(uuid4()),
                description="Prepare final response",
                action="respond",
            )
        )

        return plan

    def mark_running(self, step: TaskStep) -> None:
        step.status = StepStatus.RUNNING

    def mark_completed(
        self,
        step: TaskStep,
        result: str | None = None,
    ) -> None:
        step.status = StepStatus.COMPLETED
        step.result = result

    def mark_failed(
        self,
        step: TaskStep,
        error: str,
    ) -> None:
        step.status = StepStatus.FAILED
        step.result = error
