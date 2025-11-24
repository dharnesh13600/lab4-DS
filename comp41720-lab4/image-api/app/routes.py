from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from .helpers import(generate_image_id, save_original_image, set_status,get_status,get_processed_image,enqueue_job)
from .models import UploadResponse, StatusResponse
import base64

router = APIRouter()

# uploading new image 
@router.post("/upload-image", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    content = await file.read()
    image_id = generate_image_id()

    save_original_image(image_id, content)
    set_status(image_id, "pending")
    enqueue_job(image_id, file.filename)

    return UploadResponse(image_id = image_id, status = "pending")

#checking the status of the image
@router.get("/status/{image_id}", response_model=StatusResponse)
def status(image_id: str):
    meta = get_status(image_id)
    if not meta:
        raise HTTPException(404, "Image ID not found")
    return StatusResponse(
        image_id = image_id,
        status = meta.get("status"),
        error = meta.get("error")
    )

# getting the processed img
@router.get("/processed/{image_id}")
def processed(image_id: str):
    b64_data = get_processed_image(image_id)
    if not b64_data:
        raise HTTPException(404, "Processed image not aavailable")
    
    data = base64.b64decode(b64_data.encode("ascii"))
    return Response(content=data, media_type="image/png")
