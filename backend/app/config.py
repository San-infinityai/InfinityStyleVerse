import os

class Config:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'  # For Flask sessions or forms
    
    # Get the absolute path to the current config file directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Join the base directory with your DB filename to get absolute path
    DATABASE_PATH = os.path.join(BASE_DIR, 'infinitystyleverse.db')
    
    # Use absolute path in SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Recommended to disable, saves resources
    JWT_SECRET_KEY = 'super-secret-jwt-key'  # For JWT authentication
