from pydantic import BaseModel

class FrameMessage(BaseModel):
    """Frame from frontend"""
    data: str


class DetectionResult(BaseModel):
    "ASL detection result sent to frontend"
    sign: str
    confidence: float
    timestamp: str


