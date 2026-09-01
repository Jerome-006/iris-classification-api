from fastapi import APIRouter, HTTPException, Request
from app.config import settings
import joblib
import logging
import time
import uuid
import json

from app.models.schemas import (PredictionInput, PredictionOutput, PredictionBatchInput, PredictionBatchOutput)

router = APIRouter(prefix="/api/v1")

logger = logging.getLogger(__name__)

# Load model once
try:
    model = joblib.load(settings.MODEL_PATH)
    print("MODEL LOADED:",
settings.MODEL_PATH)
except Exception as e:
    print("MODEL LOAD ERROR:",e)
    model = None

# Load model metadata
try:
    with open(settings.MODEL_METADATA_PATH, "r") as f:
        metadata = json.load(f)
except Exception as e:
    print("METADATA LOAD ERROR:", e)
    metadata = {}


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


@router.post("/predict-batch", response_model=PredictionBatchOutput)
def predict_batch(request: Request, data: PredictionBatchInput):
    start_time = time.time()

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded"
        )

    if not data.inputs:
        raise HTTPException(
            status_code=400,
            detail="Input list cannot be empty"
        )

    if len(data.inputs) > settings.MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum batch size is {settings.MAX_BATCH_SIZE}"
        )

    try:
        # Prepare all features at once
        features = [
            [
                item.sepal_length,
                item.sepal_width,
                item.petal_length,
                item.petal_width
            ]
            for item in data.inputs
        ]

        # Predict the whole batch at once
        predictions = model.predict(features)

        confidences = [None] * len(data.inputs)

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features)
            confidences = [
                float(max(probability))
                for probability in probabilities
            ]

        results = []

        for i, prediction in enumerate(predictions):
            results.append(
                PredictionOutput(
                    prediction=int(prediction),
                    confidence=confidences[i],
                    request_id=str(uuid.uuid4())
                )
            )

        duration = time.time() - start_time

        logger.info(
            f"batch_prediction "
            f"batch_size={len(data.inputs)} "
            f"duration={duration:.4f}s"
        )

        return PredictionBatchOutput(
            predictions=results
        )

    except Exception as e:
        logger.error(
            f"batch prediction failed: {str(e)}",
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail="Batch prediction failed"
        )

@router.get("/model-info")
def model_info():
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded"
        )

    return {
        "model_type": type(model).__name__,
        "version": metadata.get("version"),
        "training_date": metadata.get("training_date"),
        "expected_features": metadata.get("expected_features"),
        "accuracy": metadata.get("accuracy")
    }