from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
import joblib
from pydantic import BaseModel
import uvicorn
from pathlib import Path

app = FastAPI(title="TaskPulseOS SLA Risk Prediction")

# Definining the input data model
class SLAPredictionRequest(BaseModel):
    sla_ms: float
    critical_path_ms: float
    attempts: int
    latency_ms: float
    queue_wait_ms: float
    step_attempts: int
    parallel_tasks_count: int

# Loading the model
try:
    BASE_DIR = Path(__file__).resolve().parents[3]
    MODEL_PATH = BASE_DIR / "models" / "taskpulseos_sla_model.pkl"
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="Model not found.")

# Define the prediction endpoint
@app.post("/predict/sla_risk")
async def predict_sla_risk(request: SLAPredictionRequest):
    # Prepare input data as a DataFrame
    input_data = {
        'sla_ms': [request.sla_ms],
        'critical_path_ms': [request.critical_path_ms],
        'attempts': [request.attempts],
        'latency_ms': [request.latency_ms],
        'queue_wait_ms': [request.queue_wait_ms],
        'step_attempts': [request.step_attempts],
        'parallel_tasks_count': [request.parallel_tasks_count]
    }
    input_df = pd.DataFrame(input_data)

    # Predict risk score
    risk_score = model.predict_proba(input_df)[:, 1][0]

    # Determine reasons (top contributing features based on coefficients)
    feature_importance = pd.DataFrame({
        'feature': input_df.columns,
        'value': input_df.iloc[0],
        'coefficient': model.coef_[0]
    })
    feature_importance['contribution'] = feature_importance['value'] * feature_importance['coefficient']
    reasons = feature_importance.sort_values(by='contribution', ascending=False).head(3).to_dict('records')

    # Prepare response
    response = {
        "risk_score": float(risk_score),  # Ensure float for JSON serialization
        "reasons": reasons
    }

    return response

# Run the app (for development; use uvicorn command for production)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)