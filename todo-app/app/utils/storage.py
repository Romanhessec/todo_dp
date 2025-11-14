import json
import os

TASKS_FILE = 'data/tasks.json'

def load_tasks():
    """Load tasks from JSON file"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)