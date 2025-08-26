from datetime import datetime
from ..database import db

class Signal(db.Model):
    __tablename__ = "signals"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    run_id = db.Column(db.Integer, db.ForeignKey("runs.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    payload_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
