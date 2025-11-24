from fastapi import FastAPI
from app.routes import router as image_router

app = FastAPI(title="Image Upload API")

app.include_router(image_router)

# health check
@app.get("/health")
def health():
    return {"status": "ok"}

