from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config')

    # Register blueprints
    from .routes.tasks import tasks_bp as tasks_blueprint
    app.register_blueprint(tasks_blueprint)

    return app