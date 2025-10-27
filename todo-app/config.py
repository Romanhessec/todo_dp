import os

class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_random_secret_key'
    JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'tasks.json')