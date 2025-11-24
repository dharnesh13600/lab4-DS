from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.worker import start_worker

@asynccontextmanager
async def lifespan(app):
    # starts the worker in the background
    start_worker()
    yield

app = FastAPI(title="Image processing worker")

@app.get("/health")
def health():
    return {"status": "ok"}
