import asyncio
import websockets
import base64
import cv2
import json


async def test():
    # Load test image
    frame = cv2.imread("tests/images/iloveyou.jpg")
    if frame is None:
        print("Image not found")
        return

    _, frame_bytes = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(frame_bytes).decode()

    print("Connecting to WebSocket...")
    async with websockets.connect("ws://localhost:8000/detection/ws") as ws:
        print("✓ Connected!")

        print("Sending frame...")
        # Convert dict to JSON string
        await ws.send(json.dumps({"data": frame_base64}))

        print("Waiting for response...")
        # Receive returns text string
        response_text = await ws.recv()
        response_dict = json.loads(response_text)

        print(f"✓ Response received:")
        print(json.dumps(response_dict, indent=2))


asyncio.run(test())