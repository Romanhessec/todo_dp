from datetime import datetime
from app import db

class Task(db.Model):
    """Simple Task model using SQLAlchemy - NO design patterns"""
    __tablename__ = 'tasks'
    
    # Simple columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def mark_completed(self):
        """Mark task as completed"""
        self.status = "completed"
    
    def mark_pending(self):
        """Mark task as pending"""
        self.status = "pending"
    
    def __repr__(self):
        return f'<Task {self.title}>'