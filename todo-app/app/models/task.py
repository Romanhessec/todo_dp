import time
from datetime import datetime

class Task:
    def __init__(self, title, description="", status="pending", task_id=None, created_at=None):
        """
        Initialize a new task
        """
        self.title = title
        self.description = description
        self.status = status
        
        # Generate unique ID if not provided
        if task_id is None:
            self.task_id = int(time.time() * 1000000)
        else:
            self.task_id = task_id
        
        # Set created_at timestamp
        if created_at is None:
            self.created_at = datetime.now().isoformat()
        else:
            self.created_at = created_at

    def mark_completed(self):
        """Mark task as completed"""
        self.status = "completed"

    def mark_pending(self):
        """Mark task as pending"""
        self.status = "pending"

    def to_dict(self):
        """Convert task to dictionary for JSON storage"""
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at
        }