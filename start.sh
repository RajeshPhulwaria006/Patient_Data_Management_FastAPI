#!/bin/sh

echo "Starting FastAPI backend..."
uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port 8000 &

echo "starting Streamlit frontend..."
streamlit run streamlit-app.py \
    --server.address=0.0.0.0 \
    --server.port=8501 \
    --server.headless=true