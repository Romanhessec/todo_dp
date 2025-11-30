from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Simple module-level instances (NO Singleton pattern)
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Initialize database
    db.init_app(app)
    
    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from .routes.tasks import tasks_bp
    from .routes.auth import auth_bp
    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID - simple function"""
    from app.models.user import User
    return User.query.get(int(user_id))