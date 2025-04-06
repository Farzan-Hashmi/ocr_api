from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.post("/ocr", response_class=PlainTextResponse)
async def ocr_image(request: Request):
    contents = await request.body()
    image = Image.open(io.BytesIO(contents))
    text = pytesseract.image_to_string(image)
    return text
