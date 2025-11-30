from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Simple module-level database instance (NO Singleton pattern)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from .routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app