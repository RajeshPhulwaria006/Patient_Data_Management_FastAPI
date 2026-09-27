#!/bin/bash

IMAGE="rajesh15phulwaria2006/patient_data_management-api:latest"
CONTAINER="patient_data_management"

API_PORT="8000"
STREAMLIT_PORT="8501"

echo "======================================"
echo " Patient Data Management Deployment"
echo "======================================"

echo ""
echo "Stopping existing container..."
docker stop "$CONTAINER" 2>/dev/null || true

echo "Removing existing container..."
docker rm "$CONTAINER" 2>/dev/null || true

echo ""
echo "Removing existing local image..."
docker image rm "$IMAGE" 2>/dev/null || true

echo ""
echo "Pulling latest image from Docker Hub..."
docker pull "$IMAGE"

echo ""
echo "Starting new container..."

docker run -d \
    --name "$CONTAINER" \
    -p "$API_PORT:8000" \
    -p "$STREAMLIT_PORT:8501" \
    "$IMAGE"

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo " Container started successfully!"
    echo "======================================"
    echo ""
    echo "Streamlit : http://localhost:$STREAMLIT_PORT"
    echo "API       : http://localhost:$API_PORT"
    echo "Swagger   : http://localhost:$API_PORT/docs"
    echo ""
    echo "Container: $CONTAINER"
    echo ""
    echo "Showing logs..."
    echo "--------------------------------------"

    docker logs -f "$CONTAINER"
else
    echo ""
    echo "Failed to start container."
    exit 1
fi