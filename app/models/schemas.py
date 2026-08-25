from pydantic import BaseModel
from typing import Optional


class PredictionInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class PredictionOutput(BaseModel):
    prediction: int
    confidence: Optional[float]
    request_id: str