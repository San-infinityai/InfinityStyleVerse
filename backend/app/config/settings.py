# backend/app/config/settings.py

class Settings:
    # Flask
    DEBUG = True
    SECRET_KEY = "dev-secret"

    # Database (update username, password, host, port, dbname)
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Nakshath7031@localhost:5432/infinitystyleversedb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = "super-secret-jwt-key"

    # Orchestrator
    ORCHESTRATOR_MOCK_MODE = True
    ORCHESTRATOR_LOG_LEVEL = "INFO"

    # HTTP Hardening
    HTTP_ALLOWED_HOSTS = ["api.example.com", "auth.example.com", "httpbin.org"]
    HTTP_ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    HTTP_REQUEST_TIMEOUT = 5.0

    # Rate Limiting
    RATE_LIMIT_PER_MIN = 60

    # Celery/Redis
    REDIS_URL = "redis://localhost:6379/0"
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL


settings = Settings()
