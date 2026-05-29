from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import logging
from prometheus_fastapi_instrumentator import Instrumentator

logging.basicConfig(level=logging.INFO, format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
logger = logging.getLogger(__name__)

app = FastAPI(title="Wine Quality API")

model = joblib.load("models/wine_quality_model.pkl")

# Metrics for Prometheus
Instrumentator().instrument(app).expose(app)

class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float
    wine_color: str

@app.post("/predict")
def predict_quality(features: WineFeatures):
    data = features.model_dump()
    data["wine_color"] = 1 if data["wine_color"] == "red" else 0
    
    df = pd.DataFrame([data])
    prediction = int(model.predict(df)[0])
    
    logger.info(f"Prediction made", extra={"features": features.model_dump(), "prediction": prediction})
    return {"quality_score": prediction}
