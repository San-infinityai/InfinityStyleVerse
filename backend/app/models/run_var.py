from ..database import db

class RunVar(db.Model):
    __tablename__ = "run_vars"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    run_id = db.Column(db.Integer, db.ForeignKey("runs.id"), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    value_json = db.Column(db.Text)
