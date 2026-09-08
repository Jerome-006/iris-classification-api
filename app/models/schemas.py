from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List


class PredictionInput(BaseModel):
    sepal_length: float = Field(gt=0, lt=100)
    sepal_width: float = Field(gt=0, lt=100)
    petal_length: float = Field(gt=0, lt=100)
    petal_width: float = Field(gt=0, lt=100)

    model_config = ConfigDict(extra="forbid")


class PredictionOutput(BaseModel):
    prediction: int
    confidence: Optional[float]
    request_id: str


class PredictionBatchInput(BaseModel):
    inputs: List[PredictionInput]


class PredictionBatchOutput(BaseModel):
    predictions: List[PredictionOutput]