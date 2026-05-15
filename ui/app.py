import streamlit as st
import requests

st.set_page_config(page_title="YOLOv8 Object Detection", layout="wide")

st.title("YOLOv8 Object Detection System")

API_URL = "https://yolov8-api-1gbv.onrender.com/detect"
IMAGE_URL = "https://yolov8-api-1gbv.onrender.com/result-image"

uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png"]
)

conf_threshold = st.slider(
    "Confidence Threshold",
    0.0,
    1.0,
    0.25
)

if st.button("Detect Objects") and uploaded_file is not None:

    files = {
        "image": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    data = {
        "confidence_threshold": conf_threshold
    }

    try:
        response = requests.post(
            API_URL,
            files=files,
            data=data
        )

        if response.status_code == 200:

            result = response.json()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Detected Image")

                image_response = requests.get(IMAGE_URL)

                if image_response.status_code == 200:
                    st.image(
                        image_response.content,
                        caption="Annotated Image",
                        use_container_width=True
                    )
                else:
                    st.write("Annotated image not available.")

            with col2:
                st.subheader("Detection Summary")
                st.json(result["summary"])

                st.subheader("Full JSON Results")
                st.json(result["detections"])

        else:
            st.error(f"API Error: {response.text}")

    except Exception as e:
        st.error(f"Connection Error: {e}")
