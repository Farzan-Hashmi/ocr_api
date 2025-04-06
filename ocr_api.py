from fastapi import FastAPI, UploadFile, File
from fastapi.responses import PlainTextResponse
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.post("/ocr", response_class=PlainTextResponse)
async def ocr_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    text = pytesseract.image_to_string(image)
    return text