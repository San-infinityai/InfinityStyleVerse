from datetime import datetime
from ..database import db

class RunStep(db.Model):
    __tablename__ = "run_steps"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    run_id = db.Column(db.Integer, db.ForeignKey("runs.id"), nullable=False)
    step_id = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    status = db.Column(db.String(50))
    attempt = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    input_json = db.Column(db.Text)
    output_json = db.Column(db.Text)
    error_json = db.Column(db.Text)
