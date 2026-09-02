from pydantic import BaseModel
from typing import List


class PredictionV2Output(BaseModel):
    prediction: int
    probabilities: List[float]
    request_id: str