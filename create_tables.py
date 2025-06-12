from sqlalchemy import create_engine
from models import Base
from server.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
