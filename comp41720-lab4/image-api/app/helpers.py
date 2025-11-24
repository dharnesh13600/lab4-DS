import redis, base64, uuid, json
from .config import settings

# connecting to redis 
r = redis.Redis(host=settings.R_HOST, port=settings.R_PORT, db=0, decode_responses=True,)

# generating a unique image id for each image
def generate_image_id():
    return str(uuid.uuid4())

# saving the original image in redis
def save_original_image(image_id: str, bytes_content: bytes):
    b64_data = base64.b64encode(bytes_content).decode("ascii")
    r.set(f"image:{image_id}:original", b64_data)

# getting processed image from redis
def get_processed_image(image_id: str):
    return r.get(f"image:{image_id}:processed")

# Updating the status of the image
def set_status(image_id: str, status: str, error=None):
    data = {"status":status}
    if error:
        data["error"] = error
    r.hset(f"image:{image_id}:meta", mapping=data)

# getting status and metadata
def get_status(image_id: str):
    return r.hgetall(f"image:{image_id}:meta")

# adding job to the queue
def enqueue_job(image_id: str, filename: str):
    job = {"image_id":image_id, "filename":filename}
    r.lpush(settings.QUEUE_NAME, json.dumps(job))