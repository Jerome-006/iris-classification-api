from app.logging_config import setup_logging
import logging
import time
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Request
import joblib
import uuid

from app.models.schemas import PredictionInput, PredictionOutput

app = FastAPI()

setup_logging()
logger = logging.getLogger(__name__)

@app.middleware("http")
async def logging_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"request_id={request_id} "
        f"method={request.method} "
        f"path={request.url.path} "
        f"duration={duration:.4f}s"
    )

    return response

class predictionError(Exception): pass

@app.exception_handler(predictionError)
async def prediction_error_handler(request, exc):
    return JSONResponse(
        status_code=500, content={
            "detail":"prediction failed"
        }
    )

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


@app.post("/predict", response_model=PredictionOutput)
def predict(request: Request,data: PredictionInput):

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

        # Confidence if model supports predict_proba
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
    f"request_id={request_id} prediction={int(prediction[0])} confidence={confidence}"
)

    return {
        "prediction": int(prediction[0]),
        "confidence": confidence,
        "request_id": request_id
    }