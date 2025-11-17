FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Google Cloud Storage client
RUN pip install --no-cache-dir google-cloud-storage

COPY getData.py .
COPY upload_to_gcs.py .

CMD ["python", "upload_to_gcs.py"]
