from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib
from pydantic import BaseModel, validator
import uvicorn
from pathlib import Path
from typing import List, Optional

app = FastAPI(title="TaskPulseOS SLA Risk Prediction")

# Loading the model
try:
    BASE_DIR = Path(__file__).resolve().parents[3]
    MODEL_PATH = BASE_DIR / "models" / "taskpulseos_sla_model.pkl"
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="Model not found.")

# Definining the input data model
class SLARiskInput(BaseModel):
    latency_ms: int
    queue_time: int
    attempt: int
    parallel_group_id: Optional[int] = None
    workflow: str
    tenant: str
    version: str
    risk: str
    sla_ms: int
    critical_path_ms: int
    hour_of_day: int

    @validator('latency_ms', 'queue_time', 'sla_ms', 'critical_path_ms', 'hour_of_day')
    def positive_values(cls, v):
        if v < 0:
            raise ValueError("Values must be non-negative")
        return v

    @validator('attempt')
    def valid_attempts(cls, v):
        if v < 0 or v > 5:
            raise ValueError("Attempt must be between 0 and 5")
        return v

    @validator('hour_of_day')
    def valid_hour(cls, v):
        if v < 0 or v > 23:
            raise ValueError("Hour must be between 0 and 23")
        return v

    @validator('workflow')
    def valid_workflow(cls, v):
        valid_workflows = ["designer_collection", "production_forecast", "retail_storefront", "sustainability_audit"]
        if v not in valid_workflows:
            raise ValueError(f"Workflow must be one of {valid_workflows}")
        return v

    @validator('tenant')
    def valid_tenant(cls, v):
        valid_tenants = ["AcmeFashion", "GlobalFactory", "TrendyRetail", "EcoWear", "LuxDesign"]
        if v not in valid_tenants:
            raise ValueError(f"Tenant must be one of {valid_tenants}")
        return v

    @validator('version')
    def valid_version(cls, v):
        valid_versions = ["v1.0", "v2.0", "v3.0"]
        if v not in valid_versions:
            raise ValueError(f"Version must be one of {valid_versions}")
        return v

    @validator('risk')
    def valid_risk(cls, v):
        valid_risks = ["ok", "watch", "at_risk", "breach"]
        if v not in valid_risks:
            raise ValueError(f"Risk must be one of {valid_risks}")
        return v

# Output data model
class SLARiskOutput(BaseModel):
    risk: float
    reasons: List[str]


@app.post("/predict/sla_risk", response_model=SLARiskOutput)
async def predict_sla_risk(input_data: SLARiskInput):
    try:
        # Converting the input to a DataFrame for model prediction
        data = pd.DataFrame([input_data.dict()])
        
        # Predicting risk score
        risk_score = model.predict_proba(data)[:, 1][0]
        
        optimal_threshold = 0.4883 

        # Generating reasons based on the feature thresholds
        reasons = []
        if data['latency_ms'][0] > 2000:
            reasons.append(f"High latency ({data['latency_ms'][0]}ms)")
        if data['queue_time'][0] > 1000:
            reasons.append(f"Long queue time ({data['queue_time'][0]}ms)")
        if data['attempt'][0] > 1:
            reasons.append(f"Multiple retries ({data['attempt'][0]})")

        # Response
        return {
            "risk": risk_score,
            "reasons": reasons if risk_score > optimal_threshold else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)