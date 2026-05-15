import os
import io
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from PIL import Image
from ultralytics import YOLO

app = FastAPI()

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "last_annotated.jpg")

model = None

def get_model():
    global model

    if model is None:
        try:
            model = YOLO("yolov8n.pt")
            print("YOLO model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")

    return model

@app.get("/")
def root():
    return {"message": "YOLO API Running"}

@app.get("/health")
def health_check():

    m = get_model()

    if m is not None:
        return {
            "status": "ok",
            "model_ready": True
        }

    return {
        "status": "error",
        "model_ready": False
    }

@app.get("/result-image")
def get_result_image():

    if os.path.exists(OUTPUT_PATH):
        return FileResponse(
            OUTPUT_PATH,
            media_type="image/jpeg"
        )

    raise HTTPException(
        status_code=404,
        detail="Image not found"
    )

@app.post("/detect")
async def detect_objects(
    image: UploadFile = File(...),
    confidence_threshold: float = Form(0.25)
):

    m = get_model()

    if m is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded."
        )

    image_bytes = await image.read()

    img = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    results = m.predict(
        img,
        conf=confidence_threshold
    )[0]

    detections = []
    summary = {}

    for b in results.boxes:

        label = results.names[int(b.cls[0])]
        score = float(b.conf[0])
        box = b.xyxy[0].tolist()

        detections.append({
            "box": box,
            "label": label,
            "score": score
        })

        summary[label] = summary.get(label, 0) + 1

    annotated_img = results.plot()

    cv2.imwrite(
        OUTPUT_PATH,
        cv2.cvtColor(
            annotated_img,
            cv2.COLOR_RGB2BGR
        )
    )

    return {
        "detections": detections,
        "summary": summary
    }
