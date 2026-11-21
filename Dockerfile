
# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /app

# Install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py download_model.py ./

# Download the latest registered model from DagsHub
ENV MODEL_NAME=digits-random-forest

RUN --mount=type=secret,id=dagshub_token,required=true \
    MLFLOW_TRACKING_USERNAME="$(cat /run/secrets/dagshub_token)" \
    MLFLOW_TRACKING_PASSWORD="" \
    python download_model.py

# Start the FastAPI application
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
