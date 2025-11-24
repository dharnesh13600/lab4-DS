import threading, json
from time import sleep
from .config import settings
from .helpers import r, set_status
from .processor import process_image

# Worker loop which waits for jobs
def worker_loop():
    print("Worker started...")
    while True:
        try:
            # blocks untill there is a new job available
            payload = r.brpop(settings.QUEUE_NAME)[1]
            job = json.loads(payload)
            image_id = job["image_id"]

            print(f"Worker Processing {image_id}")
            set_status(image_id, "processing")
            process_image(image_id)

        except Exception as e:
            print(f"Worker Error: {e}")
            sleep(1)

# starts worker in the background thread
def start_worker():
    t = threading.Thread(target=worker_loop, daemon=True)
    t.start()