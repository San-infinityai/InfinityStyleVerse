from ..database import db

class Compensation(db.Model):
    __tablename__ = "compensations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    run_id = db.Column(db.Integer, db.ForeignKey("runs.id"), nullable=False)
    step_id = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50))
    payload_json = db.Column(db.Text)
