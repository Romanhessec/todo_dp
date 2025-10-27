from flask import json
import os

class Storage:
    def __init__(self, filename='data/tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def edit_task(self, task_id, updated_task):
        for index, task in enumerate(self.tasks):
            if task['id'] == task_id:
                self.tasks[index] = updated_task
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.save_tasks()

    def get_tasks(self):
        return self.tasks