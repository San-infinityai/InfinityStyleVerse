from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .config import DATABASE_URL
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = scoped_session(sessionmaker(bind=engine))

def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
