from pydantic import BaseModel
from typing import Optional

# response after image being uploaded
class UploadResponse(BaseModel):
    image_id: str
    status: str

# respose we get when checking the img status
class StatusResponse(BaseModel):
    image_id: str
    status: str
    error: Optional[str] = None