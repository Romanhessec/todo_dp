import json
import os
from app.models.task import Task

DATA_FILE = 'data/tasks.json'

TASKS_FILE = 'data/tasks.json'

def load_tasks():
    """Load tasks from JSON file"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            data = json.load(file)
            return [Task(
                title=task['title'],
                description=task.get('description', ''),
                status=task.get('status', 'pending'),
                task_id=task.get('id'),
                created_at=task.get('created_at')
            ) for task in data]
    return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    # Ensure directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    with open(DATA_FILE, 'w') as file:
        # Convert Task objects to dictionaries
        tasks_data = [task.to_dict() if hasattr(task, 'to_dict') else task for task in tasks]
        json.dump(tasks_data, file, indent=4)