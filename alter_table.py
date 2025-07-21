# from backend.app import create_app
# from backend.app.database import db
from sqlalchemy import text
from backend.app import create_app
from backend.app.database import db

app = create_app()

with app.app_context():
    with db.engine.connect() as conn:
        # Add image_url column (nullable to avoid breaking existing rows)
        conn.execute(text(
            "ALTER TABLE user ADD COLUMN image_url LONGBLOB;"
        ))
        print("Added 'image_url' column.")

        # Add image_mime column (nullable to avoid errors on existing rows)
        conn.execute(text(
            "ALTER TABLE user ADD COLUMN image_mime VARCHAR(50) NULL;"
        ))
        print("Added 'image_mime' column.")
