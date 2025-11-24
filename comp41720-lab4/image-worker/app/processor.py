from PIL import Image, ImageDraw, ImageFont
import io
from .helpers import get_original, save_processed, set_status
import base64

def process_image(image_id: str):
    b64_original = get_original(image_id)
    if not b64_original:
        set_status(image_id, "failed", "Original image missing")
        return
    
    raw = base64.b64decode(b64_original.encode("ascii"))
    image = Image.open(io.BytesIO(raw)).convert("RGB")

    # greyscale
    image = image.convert("L").convert("RGB")

    # resize
    image.thumbnail((300, 300))

    # Watermark
    draw = ImageDraw.Draw(image)
    text = "LAB-4"
    font = ImageFont.load_default()
    draw.text((10, image.height - 20), text, fill=(255,0,0), font=font)

    out = io.BytesIO()
    image.save(out, format = "PNG")
    out.seek(0)

    save_processed(image_id, out.read())
    set_status(image_id, "processed")