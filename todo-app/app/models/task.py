import time

class Task:
    def __init__(self, title, description="", status="pending", task_id=None):
        self.id = task_id if task_id else int(time.time() * 1000000)  # Generate unique ID based on timestamp
        self.title = title
        self.description = description
        self.status = status

    def mark_completed(self):
        self.status = "completed"

    def mark_pending(self):
        self.status = "pending"

    def update_description(self, new_description):
        self.description = new_description

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }