# SLRS Backend : SignBridge

FastAPI backend powering real-time American Sign Language (ASL) detection over WebSocket, using a DETR-based detection model (SignDETR).

## Overview

This service accepts a live video frame stream from a connected frontend over WebSocket, runs each frame through a trained object-detection model, and returns the detected sign along with a confidence score in real time.

Built as the backend for **SignBridge**, a real-time ASL recognition web app. The frontend (React/Vite) lives in a separate repository.

## Tech Stack

- **FastAPI** : HTTP + WebSocket server
- **Uvicorn** : ASGI server
- **PyTorch / TorchVision** : model inference
- **OpenCV / Albumentations** : image decoding and preprocessing
- **Docker** : containerized deployment
- **Render** : hosting

## Architecture
Frontend (browser)
│ binary JPEG frames over WebSocket
▼
FastAPI WebSocket route (/detection/ws)
│
▼
SignDETRHandler — decodes frame, runs inference
│
▼
JSON response: { "sign": "...", "confidence": 0.95, "timestamp": "..." }

# Project Structure
.
├── app/
│ ├── ml/
│ │ ├── signdetr_handler.py # loads model, runs inference
│ │ └── vendor/ # vendored inference-only SignDETR code
│ │ ├── model.py
│ │ ├── config.json
│ │ ├── pretrained/ # model weights (fetched at build time)
│ │ └── utils/ # logging/display helpers
│ ├── routers/
│ │ └── detection.py # WebSocket route
│ ├── schemas/
│ │ └── detection.py # Pydantic response models
│ └── utils/
│ └── frame_decoder.py # bytes → image array
├── tests/
├── main.py # FastAPI app entrypoint
├── requirements.txt
├── Dockerfile
└── README.md

## Local Development

**Requirements:** Python 3.12, a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, WebSocket at `ws://127.0.0.1:8000/detection/ws`.

## Running with Docker

```bash
docker build -t signbridge-backend .
docker run -p 8000:8000 signbridge-backend
```

The Docker build fetches pretrained model weights automatically from a GitHub Release during the build step — no manual download needed.

## WebSocket API

**Endpoint:** `/detection/ws`

**Client → Server:** binary JPEG frame (raw bytes, not base64)

**Server → Client:**
```json
{
  "sign": "Hello",
  "confidence": 0.95,
  "timestamp": "2026-09-24T10:55:38.783Z"
}
```

## Configuration

Allowed WebSocket origins are set in `app/routers/detection.py` and CORS origins in `main.py`. Update both when adding a new frontend deployment URL.

## Deployment

Deployed on Render as a Docker web service, auto-deploying on every push to `main`. Health check: `GET /`.

## Model

Inference uses a DETR (Detection Transformer) model with a ResNet-50 backbone, adapted for sign classification. Only the inference-relevant code (`model.py`, `config.json`, minimal logging utilities) is vendored into this repo — training code and datasets live in the full [SignDETR](https://github.com/<your-username>/SignDETR) repository.

## Acknowledgements

The SignDETR model architecture is based on work by Nick Renotte, MIT licensed. This repository builds the FastAPI backend and deployment pipeline around it; the model architecture and training approach are his original work.

## License

MIT
