import redis, base64
from .config import settings

# Connecting to redis
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True,)

# update img status
def set_status(image_id: str, status: str, error: str | None = None):
    data = {"status": status}
    if error:
        data["error"] = error
    r.hset(f"image:{image_id}:meta", mapping=data)

# getting the original image 
def get_original(image_id: str):
    return r.get(f"image:{image_id}:original")

# save processed img
def save_processed(image_id: str, img_bytes: bytes):
    b64 = base64.b64encode(img_bytes).decode("ascii")
    r.set(f"image:{image_id}:processed", b64)

 