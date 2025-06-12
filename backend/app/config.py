class Config:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'

DATABASE_URL = 'mysql+pymysql://root:@localhost/infinitystyleverse_db'

class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret-jwt-key'
