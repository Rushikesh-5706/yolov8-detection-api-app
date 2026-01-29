import streamlit as st
import requests
from PIL import Image
import io
import os

st.set_page_config(page_title="YOLOv8 Object Detection", layout="wide")
st.title("YOLOv8 Object Detection System")

# Get API URL from environment or default to localhost
API_URL = os.getenv("API_URL", "http://api:8000/detect")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.25)

if st.button("Detect Objects") and uploaded_file is not None:
    files = {"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    data = {"confidence_threshold": conf_threshold}
    
    try:
        response = requests.post(API_URL, files=files, data=data)
        if response.status_code == 200:
            result = response.json()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Detected Image")
                # Look for the persisted image from the shared volume
                if os.path.exists("/app/output/last_annotated.jpg"):
                    st.image("/app/output/last_annotated.jpg")
                else:
                    st.write("Processing complete. View JSON summary for details.")
                    
            with col2:
                st.subheader("Detection Summary")
                st.json(result["summary"])
                st.subheader("Full JSON Results")
                st.json(result["detections"])
        else:
            st.error(f"API Error: {response.text}")
    except Exception as e:
        st.error(f"Connection Error: {e}")
