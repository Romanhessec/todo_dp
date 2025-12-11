"""Command pattern implementation to enable undo/redo for task operations."""
from __future__ import annotations
from typing import List, Protocol, Optional, Any, Dict
from app import db
from app.models.task import Task
from app.patterns.observer import TaskEvent


class Command(Protocol):
    def execute(self) -> None:
        ...

    def undo(self) -> None:
        ...


class CommandHistory:
    def __init__(self) -> None:
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self) -> Optional[Command]:
        if not self._undo_stack:
            return None
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)
        return command

    def redo(self) -> Optional[Command]:
        if not self._redo_stack:
            return None
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)
        return command

    @property
    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo_stack)


class AddTaskCommand:
    def __init__(self, data_manager, task: Task):
        self.data_manager = data_manager
        self.task = task
        self.task_id: Optional[int] = None

    def execute(self) -> None:
        db.session.add(self.task)
        db.session.commit()
        self.task_id = self.task.id
        self.data_manager.notify(TaskEvent("task_added", self.task.user_id, self.task.id))

    def undo(self) -> None:
        task = Task.query.get(self.task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            self.data_manager.notify(TaskEvent("task_removed", task.user_id, self.task_id))


class DeleteTaskCommand:
    def __init__(self, data_manager, task: Task):
        self.data_manager = data_manager
        self.task_id = task.id
        self.user_id = task.user_id
        # Store a snapshot of task data instead of the object reference
        self.task_data: Dict[str, Any] = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "task_type": task.task_type,
            "user_id": task.user_id,
            "created_at": task.created_at,
        }

    def execute(self) -> None:
        task = Task.query.get(self.task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            self.data_manager.notify(TaskEvent("task_deleted", self.user_id, self.task_id))

    def undo(self) -> None:
        # Recreate the task from snapshot data
        task = Task(
            id=self.task_data["id"],
            title=self.task_data["title"],
            description=self.task_data["description"],
            status=self.task_data["status"],
            task_type=self.task_data["task_type"],
            user_id=self.task_data["user_id"],
            created_at=self.task_data["created_at"],
        )
        db.session.add(task)
        db.session.commit()
        self.data_manager.notify(TaskEvent("task_restored", self.user_id, self.task_id))


class ToggleTaskCommand:
    def __init__(self, data_manager, task: Task):
        self.data_manager = data_manager
        self.task_id = task.id
        self.user_id = task.user_id
        self.previous_status = task.status

    def execute(self) -> None:
        task = Task.query.get(self.task_id)
        if task:
            task.status = "completed" if task.status == "pending" else "pending"
            db.session.commit()
            self.data_manager.notify(TaskEvent("task_toggled", self.user_id, self.task_id))

    def undo(self) -> None:
        task = Task.query.get(self.task_id)
        if task:
            task.status = self.previous_status
            db.session.commit()
            self.data_manager.notify(TaskEvent("task_toggle_undone", self.user_id, self.task_id))


class EditTaskCommand:
    def __init__(self, data_manager, task: Task, new_title: str, new_description: str):
        self.data_manager = data_manager
        self.task_id = task.id
        self.user_id = task.user_id
        self.old_title = task.title
        self.old_description = task.description
        self.new_title = new_title
        self.new_description = new_description

    def execute(self) -> None:
        task = Task.query.get(self.task_id)
        if task:
            task.edit(title=self.new_title, description=self.new_description)
            db.session.commit()
            self.data_manager.notify(TaskEvent("task_edited", self.user_id, self.task_id))

    def undo(self) -> None:
        task = Task.query.get(self.task_id)
        if task:
            task.edit(title=self.old_title, description=self.old_description)
            db.session.commit()
            self.data_manager.notify(TaskEvent("task_edit_undone", self.user_id, self.task_id))
