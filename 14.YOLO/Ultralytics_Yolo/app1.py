import streamlit as st
import cv2
from ultralytics import YOLO
import tempfile
import numpy as np
from PIL import Image
import base64

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="DeepVision Analyzer", layout="wide", page_icon="🤖")

# -----------------------------------
# OPTIONAL BACKGROUND VIDEO
# -----------------------------------
def add_bg_video(video_path):
    with open(video_path, "rb") as video_file:
        video_bytes = video_file.read()
    base64_video = base64.b64encode(video_bytes).decode("utf-8")

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
            color: white;
        }}
        video {{
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%;
            min-height: 100%;
            z-index: -1;
            filter: brightness(30%);
        }}
        </style>
        <video autoplay muted loop playsinline>
            <source src="data:video/mp4;base64,{base64_video}" type="video/mp4">
        </video>
        """,
        unsafe_allow_html=True,
    )

# add_bg_video("background.mp4")  # Uncomment if needed


# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
    <style>
    .big-title {
        text-align: center;
        font-size: 50px;
        font-weight: 700;
        color: #4A90E2;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #B0BEC5;
        font-size: 18px;
        margin-bottom: 30px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #4A90E2, #9013FE);
        color: white;
        border-radius: 10px;
        border: none;
        font-size: 18px;
        font-weight: bold;
        padding: 10px 30px;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(45deg, #9013FE, #4A90E2);
    }
    </style>
""", unsafe_allow_html=True)


# -----------------------------------
# MAIN DETECTION APP
# -----------------------------------
def detection_app():
    st.markdown("<h1 class='big-title'>DeepVision Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Perform Multi-Model Detection: Object Detection, Pose, Segmentation, and More</p>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("⚙️ Configuration")

        model_options = st.multiselect(
            "Select Models to Run",
            ["Detection", "Segmentation", "Pose", "Tracking", "Counting"],
            default=["Detection"]
        )

        confidence = st.slider("Confidence Threshold", 0.1, 1.0, 0.5, 0.05)

        model_paths = {
            "Detection": "yolov8n.pt",
            "Segmentation": "yolov8n-seg.pt",
            "Pose": "yolov8n-pose.pt",
            "Tracking": "yolov8n.pt",
            "Counting": "yolov8n.pt",
        }

        loaded_models = {m: YOLO(model_paths[m]) for m in model_options}
        st.success(f"Loaded Models: {', '.join(model_options)}")

        input_source = st.radio("Select Input Type", ["🖼️ Image Upload", "🎞️ Video Upload", "📷 Webcam"])

    # -----------------------------------
    # IMAGE MODE
    # -----------------------------------
    if input_source == "🖼️ Image Upload":
        st.write("Upload an image below to start detection using multiple models.")
        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            if st.button("Start Multi-Model Detection"):
                with st.spinner("Processing Image..."):
                    frame = np.array(image)
                    for name, model in loaded_models.items():
                        results = model(frame, conf=confidence)
                        frame = results[0].plot()
                    st.image(frame, caption="Combined Detection Output", use_container_width=True)
                    img_bytes = cv2.imencode('.jpg', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))[1].tobytes()
                    st.download_button("Download Result", data=img_bytes, file_name="output_multi.jpg")

    # -----------------------------------
    # VIDEO MODE
    # -----------------------------------
    elif input_source == "🎞️ Video Upload":
        st.write("Upload a video below to start detection using multiple models.")
        uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
        if uploaded_video:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_video.read())
            video_path = tfile.name

            if st.button("Start Multi-Model Detection"):
                cap = cv2.VideoCapture(video_path)
                stframe = st.empty()
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
                processed = 0
                progress = st.progress(0)

                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                output_path = "processed_output_multi.mp4"
                writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    for name, model in loaded_models.items():
                        results = model(frame, conf=confidence)
                        frame = results[0].plot()
                    writer.write(frame)
                    processed += 1
                    progress.progress(min(processed / frame_count, 1.0))
                    stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)

                cap.release()
                writer.release()
                st.success("✅ Multi-Model Video Detection Completed!")
                with open(output_path, "rb") as f:
                    st.download_button("Download Processed Video", f, file_name="result_multi.mp4")

    # -----------------------------------
    # WEBCAM MODE
    # -----------------------------------
    elif input_source == "📷 Webcam":
        st.write("Click below to start live detection using multiple models.")
        if st.button("Start Multi-Model Webcam Detection"):
            cap = cv2.VideoCapture(0)
            stframe = st.empty()
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                for name, model in loaded_models.items():
                    results = model(frame, conf=confidence)
                    frame = results[0].plot()
                stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
            cap.release()

    st.write("---")
    st.markdown("<p style='text-align:center;'>| DeepVision Analyzer | Powered by YOLOv8 | Multi-Model Mode Enabled 🧠</p>", unsafe_allow_html=True)


# Run the app
if __name__ == "__main__":
    detection_app()
