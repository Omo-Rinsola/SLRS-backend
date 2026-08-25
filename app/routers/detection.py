from fastapi import APIRouter, WebSocket
from app.schemas.detection import DetectionResult
from app.ml.signdetr_handler import SignDETRHandler
from app.utils.frame_decoder import decode_frame
from datetime import datetime

ALLOWED_ORIGINS = {
    "http://localhost:5173",
    "https://your-frontend.vercel.app",
}

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
    origin = websocket.headers.get("origin")
    if origin not in ALLOWED_ORIGINS:
        await websocket.close(code=1008)
        return

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

