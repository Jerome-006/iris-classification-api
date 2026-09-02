from fastapi import APIRouter, HTTPException, Request
from app.config import settings
from app.models.schemas import PredictionInput
from app.models.schemas_v2 import PredictionV2Output

import joblib
import logging
import uuid


router = APIRouter(prefix="/api/v2")

logger = logging.getLogger(__name__)


# Load model
try:
    model = joblib.load(settings.MODEL_PATH)
    print("V2 MODEL LOADED:", settings.MODEL_PATH)
except Exception as e:
    print("V2 MODEL LOAD ERROR:", e)
    model = None


@router.post("/predict", response_model=PredictionV2Output)
def predict_v2(request: Request, data: PredictionInput):

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

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features)[0]
            probabilities = [
                float(probability)
                for probability in probabilities
            ]
        else:
            probabilities = []

    except Exception as e:
        logger.error(
            f"request_id={request.state.request_id} "
            f"v2 prediction failed",
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail="V2 prediction failed"
        )

    request_id = request.state.request_id

    logger.info(
        f"request_id={request_id} "
        f"v2_prediction={int(prediction[0])} "
        f"probabilities={probabilities}"
    )

    return {
        "prediction": int(prediction[0]),
        "probabilities": probabilities,
        "request_id": request_id
    }