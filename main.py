from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import detection

app = FastAPI(
    title="SignBridge",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"'message": "Welcome to SignBridge"}

app.include_router(detection.router)
