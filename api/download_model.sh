#!/bin/bash
mkdir -p /app/models
MODEL_URL="https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt"
wget -O /app/models/yolov8n.pt $MODEL_URL
# Grant read permissions so the Python app can load it
chmod 644 /app/models/yolov8n.pt
