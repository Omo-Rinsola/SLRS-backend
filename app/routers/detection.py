from fastapi import APIRouter, WebSocket
from app.schemas.detection import DetectionResult
from app.ml.signdetr_handler import SignDETRHandler
from app.utils.frame_decoder import decode_frame
from datetime import datetime

router = APIRouter(
    prefix="/detection",
    tags=["detection"],
    responses={404: {"description": "Not found"}},
)
handler = SignDETRHandler()


@router.websocket("/ws")
async def websocket_detection(websocket: WebSocket):
    """
        WebSocket endpoint for real-time sign detection

        Frontend sends: {"data": "base64_frame"}
        Backend sends: {"sign": "Hello", "confidence": 0.95, "timestamp": "..."}
        """
    await websocket.accept()
    while True:
        message = await websocket.receive_bytes()
        frame = decode_frame(message)


        # DETECT IMAGE
        sign, best_confidence = handler.detect(frame)
        local_time = datetime.now().isoformat()
        response_data = DetectionResult(
            sign=sign,
            confidence=best_confidence,
            timestamp=local_time
        )

        await websocket.send_json(response_data.model_dump())

