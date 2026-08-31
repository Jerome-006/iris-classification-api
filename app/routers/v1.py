from fastapi import APIRouter, HTTPException, Request
import joblib
import logging

from app.models.schemas import PredictionInput, PredictionOutput

router = APIRouter(prefix="/api/v1")

logger = logging.getLogger(__name__)

# Load model once
try:
    model = joblib.load("ml/saved_model/model.joblib")
except Exception:
    model = None


@router.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None
    }


@router.post("/predict", response_model=PredictionOutput)
def predict(request: Request, data: PredictionInput):

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded"
        )

    try:
        features = [[
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width
        ]]

        prediction = model.predict(features)

        confidence = None

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features)
            confidence = float(max(probabilities[0]))

    except Exception as e:
        logger.error(
            f"request_id={request.state.request_id} prediction failed",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

    request_id = request.state.request_id

    logger.info(
        f"request_id={request_id} "
        f"prediction={int(prediction[0])} "
        f"confidence={confidence}"
    )

    return {
        "prediction": int(prediction[0]),
        "confidence": confidence,
        "request_id": request_id
    }