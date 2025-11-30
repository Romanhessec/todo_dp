from app import db
from app.models.task import Task

def load_tasks():
    """Load all tasks from database - simple function"""
    return Task.query.all()

def save_task(task):
    """Save a single task to database - simple function"""
    db.session.add(task)
    db.session.commit()

def delete_task(task):
    """Delete a task from database - simple function"""
    db.session.delete(task)
    db.session.commit()

def update_task():
    """Commit changes to database - simple function"""
    db.session.commit()