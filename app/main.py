from fastapi import FastAPI, HTTPException
import joblib
import uuid

from app.models.schemas import PredictionInput

app = FastAPI()

# Load model only once at startup
try:
    model = joblib.load("ml/saved_model/model.joblib")
except Exception:
    model = None


@app.get("/")
def home():
    return {"message": "Iris API running"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None
    }


@app.post("/predict")
def predict(data: PredictionInput):

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded"
        )

    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    prediction = model.predict(features)

    # Confidence if model supports predict_proba
    confidence = None

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(features)
        confidence = float(max(probabilities[0]))

    request_id = str(uuid.uuid4())

    return {
        "prediction": int(prediction[0]),
        "confidence": confidence,
        "request_id": request_id
    }