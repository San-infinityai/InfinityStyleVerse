from backend.app import create_app
from backend.app.database import db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database reset complete!")
