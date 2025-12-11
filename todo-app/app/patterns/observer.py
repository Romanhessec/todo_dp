"""Observer pattern to react to task lifecycle events."""
from dataclasses import dataclass
from typing import Protocol, Optional


@dataclass
class TaskEvent:
    action: str
    user_id: int
    task_id: Optional[int] = None


class TaskObserver(Protocol):
    def update(self, event: TaskEvent) -> None:
        ...


class StatsObserver:
    """Recomputes stats cache whenever a task changes."""

    def __init__(self, data_manager):
        self.data_manager = data_manager

    def update(self, event: TaskEvent) -> None:
        self.data_manager.refresh_stats(event.user_id)


class AuditObserver:
    """Minimal audit trail; could be wired to logging/metrics later."""

    def __init__(self, emitter):
        self.emitter = emitter

    def update(self, event: TaskEvent) -> None:
        message = f"AUDIT: {event.action} for user={event.user_id} task={event.task_id}"
        self.emitter(message)
