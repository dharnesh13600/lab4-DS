import os

# loading settings from env variables
class Settings:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    QUEUE_NAME = os.getenv("QUEUE_NAME", "image_jobs")

settings = Settings()