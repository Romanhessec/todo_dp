"""Storage/DataManager module now driven by GoF patterns."""
from collections import defaultdict
from flask import abort
from app import db
from app.models.task import Task
from app.patterns.singleton import SingletonMeta
from app.patterns.factory import TaskFactory
from app.patterns.command import (
    CommandHistory,
    AddTaskCommand,
    ToggleTaskCommand,
    DeleteTaskCommand,
    EditTaskCommand,
)
from app.patterns.observer import TaskEvent


class DataManager(metaclass=SingletonMeta):
    """Centralizes task persistence with Singleton + Command + Observer."""

    def __init__(self) -> None:
        self._observers = []
        self._histories = defaultdict(CommandHistory)
        self._stats_cache = {}

    # Observer helpers
    def register_observer(self, observer) -> None:
        self._observers.append(observer)

    def notify(self, event: TaskEvent) -> None:
        for observer in self._observers:
            observer.update(event)

    # History helpers
    def _history(self, user_id: int) -> CommandHistory:
        return self._histories[user_id]

    def undo(self, user_id: int):
        return self._history(user_id).undo()

    def redo(self, user_id: int):
        return self._history(user_id).redo()

    # Stats helpers
    def refresh_stats(self, user_id: int):
        tasks = Task.query.filter_by(user_id=user_id).all()
        self._stats_cache[user_id] = {
            "total": len(tasks),
            "completed": len([t for t in tasks if t.status == "completed"]),
            "pending": len([t for t in tasks if t.status == "pending"]),
        }
        return self._stats_cache[user_id]

    def get_stats(self, user_id: int):
        if user_id not in self._stats_cache:
            return self.refresh_stats(user_id)
        return self._stats_cache[user_id]

    # Query helpers
    def get_tasks(self, user_id: int, filter_status: str = "all", filter_type: str = "all", sort_by: str = "none"):
        tasks = Task.query.filter_by(user_id=user_id).all()

        if filter_status == "pending":
            tasks = [t for t in tasks if t.status == "pending"]
        elif filter_status == "completed":
            tasks = [t for t in tasks if t.status == "completed"]

        if filter_type != "all":
            tasks = [t for t in tasks if t.task_type == filter_type]

        if sort_by == "title":
            tasks = sorted(tasks, key=lambda x: x.title.lower())
        elif sort_by == "status":
            tasks = sorted(tasks, key=lambda x: (x.status, x.title.lower()))

        return tasks

    def get_task_for_user(self, task_id: int, user_id: int) -> Task:
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            abort(404)
        return task

    # Command-based operations
    def add_task(self, user_id: int, title: str, description: str, task_type: str = "simple") -> Task:
        task = TaskFactory.create_task(task_type, title=title, description=description, user_id=user_id)
        history = self._history(user_id)
        history.execute(AddTaskCommand(self, task))
        return task

    def toggle_task(self, user_id: int, task_id: int) -> Task:
        task = self.get_task_for_user(task_id, user_id)
        history = self._history(user_id)
        history.execute(ToggleTaskCommand(self, task))
        return task

    def delete_task(self, user_id: int, task_id: int) -> Task:
        task = self.get_task_for_user(task_id, user_id)
        history = self._history(user_id)
        history.execute(DeleteTaskCommand(self, task))
        return task

    def edit_task(self, user_id: int, task_id: int, new_title: str, new_description: str) -> Task:
        task = self.get_task_for_user(task_id, user_id)
        history = self._history(user_id)
        history.execute(EditTaskCommand(self, task, new_title, new_description))
        return task

    def clear_completed(self, user_id: int) -> None:
        completed_tasks = Task.query.filter_by(user_id=user_id, status="completed").all()
        for task in completed_tasks:
            self._history(user_id).execute(DeleteTaskCommand(self, task))

    # Expose history state to the UI
    def history_state(self, user_id: int) -> dict:
        history = self._history(user_id)
        return {"can_undo": history.can_undo, "can_redo": history.can_redo}