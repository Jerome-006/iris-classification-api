from pydantic import BaseModel
from typing import Optional,List


class PredictionInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class PredictionOutput(BaseModel):
    prediction: int
    confidence: Optional[float]
    request_id: str


class PredictionBatchInput(BaseModel):
    inputs: List[PredictionInput]


class PredictionBatchOutput(BaseModel):
    predictions: List[PredictionOutput]