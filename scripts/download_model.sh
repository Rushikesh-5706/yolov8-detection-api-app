#!/bin/bash
mkdir -p models
MODEL_URL="https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt"
if [ ! -f models/yolov8n.pt ]; then
    echo "Downloading YOLOv8n model..."
    curl -L -o models/yolov8n.pt $MODEL_URL
    echo "Model downloaded successfully to models/yolov8n.pt"
else
    echo "Model already exists."
fi
