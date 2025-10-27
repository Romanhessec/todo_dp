import pytest
from app.models.task import Task

def test_task_creation():
    task = Task(title="Test Task", description="This is a test task.")
    assert task.title == "Test Task"
    assert task.description == "This is a test task."
    assert task.status == "pending"

def test_task_mark_completed():
    task = Task(title="Test Task", description="This is a test task.")
    task.mark_completed()
    assert task.status == "completed"

def test_task_edit():
    task = Task(title="Test Task", description="This is a test task.")
    task.edit(title="Updated Task", description="Updated description.")
    assert task.title == "Updated Task"
    assert task.description == "Updated description."

def test_task_to_dict():
    task = Task(title="Test Task", description="This is a test task.")
    task_dict = task.to_dict()
    assert task_dict == {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "pending"
    }