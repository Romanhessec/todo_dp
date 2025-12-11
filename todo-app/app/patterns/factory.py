"""Factory Method for creating Task instances with different presets."""
from datetime import datetime, timedelta
from typing import Protocol
from app.models.task import Task


class TaskCreator(Protocol):
    def create(self, **kwargs) -> Task:
        ...


class SimpleTaskCreator:
    def create(self, **kwargs) -> Task:
        return Task(**kwargs, task_type="simple")


class PriorityTaskCreator:
    def create(self, **kwargs) -> Task:
        # Prepend a subtle marker instead of changing schema further
        description = kwargs.get("description", "").strip()
        marker = "[PRIORITY] "
        kwargs["description"] = f"{marker}{description}".strip()
        return Task(**kwargs, task_type="priority")


class RecurringTaskCreator:
    def create(self, **kwargs) -> Task:
        # Add a hint when the next instance should occur
        description = kwargs.get("description", "").strip()
        next_run = datetime.utcnow() + timedelta(days=7)
        hint = f"(next occurrence on {next_run.date()})"
        kwargs["description"] = " ".join([description, hint]).strip()
        return Task(**kwargs, task_type="recurring")


class TaskFactory:
    _creators = {
        "simple": SimpleTaskCreator(),
        "priority": PriorityTaskCreator(),
        "recurring": RecurringTaskCreator(),
    }

    @classmethod
    def create_task(cls, task_type: str, **kwargs) -> Task:
        creator = cls._creators.get(task_type, cls._creators["simple"])
        return creator.create(**kwargs)
