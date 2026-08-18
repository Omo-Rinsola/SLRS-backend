from pydantic import BaseModel
from typing import Optional

class DetectionResult(BaseModel):
    "ASL detection result sent to frontend"
    sign: Optional[str]
    confidence: float
    timestamp: str


