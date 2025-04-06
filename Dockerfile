# Use official Python image
FROM python:3.11-slim

# Install Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr && apt-get clean

# Set working directory
WORKDIR /app

# Copy files and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "ocr_api:app", "--host", "0.0.0.0", "--port", "8080"]
