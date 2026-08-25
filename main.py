from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import detection

app = FastAPI(
    title="SignBridge",
)

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://your-frontend.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"'message": "Welcome to SignBridge"}

app.include_router(detection.router)
