import os
from datetime import timedelta

class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # For Flask sessions or forms
    
    # Get the absolute path to the current config file directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Join the base directory with your DB filename to get absolute path
    DATABASE_PATH = os.path.join(BASE_DIR, 'infinitystyleverse.db')
    
    # Use absolute path in SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Recommended to disable, saves resources
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-prod")
    JWT_ALGORITHM = "HS256"
    JWT_TOKEN_LOCATION = ["headers"]          
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Access token validity
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)    # Refresh token validity

    # Optional: for development testing without frontend deployment
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
    CORS_SUPPORTS_CREDENTIALS = True

    # SeaSurf (CSRF)
    # Cookie is intentionally NOT HttpOnly so the frontend can read and echo it in a header
    SEASURF_COOKIE_NAME = "XSRF-TOKEN"
    SEASURF_HEADER_NAME = "X-CSRFToken"  # also accepts X-CSRF-Token
    SEASURF_COOKIE_SAMESITE = "Lax"
    SEASURF_COOKIE_SECURE = False  # True in production (HTTPS)