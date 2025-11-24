import os

# loading settings from env variables
class Settings:
    R_HOST = os.getenv("R_HOST", "localhost")
    R_PORT = int(os.getenv("R_PORT", "6379"))
    QUEUE_NAME = os.getenv("QUEUE_NAME", "image_jobs")

settings = Settings()
