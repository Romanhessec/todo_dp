import os

class Config:
    """Database configuration - simple settings, no design patterns"""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://todouser:todopass@localhost:5432/todoapp'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
