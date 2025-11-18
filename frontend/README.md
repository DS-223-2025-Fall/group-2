# Frontend – Streamlit UI Skeleton

This directory contains the frontend service for the Marketing Analytics group project. It includes a basic Streamlit UI skeleton and a Docker setup so the app can be run locally or inside a container.

## Project Structure
```
frontend/
│
├── app.py              # Streamlit application (UI skeleton)
├── requirements.txt    # Python dependencies
└── Dockerfile          # Container configuration for frontend service
```

## Running the Frontend
### 1. Run Locally (without Docker)

Make sure you have Python 3.10+ installed.
```
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### 2. Running with Docker

#### Build the Docker image

From the root of the project:
``` bash
docker build -t frontend-service ./frontend
```
Run the container
``` bash
docker run --rm -p 8501:8501 frontend-service
```

## Dockerfile Summary

The Dockerfile:

- Uses `python:3.11-slim`
- Installs all dependencies from `requirements.txt`
- Copies the Streamlit app into `/app`
- Runs the app on port `8501`

