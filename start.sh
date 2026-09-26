#!/bin/bash

IMAGE="rajesh15phulwaria2006/patient_data_management-api"
CONTAINER="patient_data_management"
PORT="8000"

echo "Pulling latest Docker image..."
docker pull "$IMAGE:latest"

echo "Stopping existing container if running..."
docker stop "$CONTAINER" 2>/dev/null || true

echo "Removing existing container..."
docker rm "$CONTAINER" 2>/dev/null || true

echo "Starting container..."
docker run -d \
    --name "$CONTAINER" \
    -p "$PORT:8000" \
    "$IMAGE:latest"

echo "Container started successfully!"
echo "API: http://localhost:$PORT"
echo "Swagger Docs: http://localhost:$PORT/docs"

docker logs -f patient_data_management

docker stop patient_data_management
