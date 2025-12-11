from datetime import datetime
from app import db


class Task(db.Model):
    """Task entity that can be instantiated via the TaskFactory (Factory Method)."""
    __tablename__ = 'tasks'

    # Core columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    status = db.Column(db.String(20), default='pending')
    task_type = db.Column(db.String(50), default='simple')  # used by the Factory Method
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def mark_completed(self):
        """Mark task as completed."""
        self.status = "completed"

    def mark_pending(self):
        """Mark task as pending."""
        self.status = "pending"

    def edit(self, title=None, description=None):
        """Update editable fields in-place (used by EditTaskCommand)."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description

    def to_dict(self):
        """Serialize a minimal view used by tests and history snapshots."""
        return {
            "title": self.title,
            "description": self.description,
            "status": self.status,
        }

    def __repr__(self):
        return f'<Task {self.title}>'