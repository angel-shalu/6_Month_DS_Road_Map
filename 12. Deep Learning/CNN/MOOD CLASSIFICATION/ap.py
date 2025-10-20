import os
from pathlib import Path
from io import BytesIO
from PIL import Image
import streamlit as st

from model import MoodModel  # make sure model.py is in the same folder


# --- Basic Paths ---
BASE_DIR = Path(__file__).parent
WEIGHTS_FILE = BASE_DIR / "mood_weights.h5"
TRAIN_DIR = BASE_DIR / "trainning"  # sample dataset folder


# --- Helper function to load sample dataset images ---
def load_samples(folder):
    samples = []
    for mood in ["happy", "not happy"]:
        mood_folder = folder / mood
        if mood_folder.exists():
            for img_path in mood_folder.glob("*.[jp][pn]g"):
                samples.append((mood, img_path))
    return samples


# --- Initialize model (only once) ---
if "model" not in st.session_state:
    st.session_state["model"] = MoodModel(str(WEIGHTS_FILE) if WEIGHTS_FILE.exists() else None)
model = st.session_state["model"]


# --- App layout ---
st.set_page_config(page_title="Mood Classifier", layout="wide", page_icon="😊")

# --- Custom CSS for Top Navigation Bar ---
st.markdown("""
    <style>
    .nav {
        background-color: #f0f2f6;
        padding: 12px;
        text-align: center;
        border-radius: 8px;
        margin-bottom: 25px;
    }
    .nav a {
        text-decoration: none;
        color: #000;
        margin: 0 20px;
        font-weight: 600;
        font-size: 18px;
        transition: 0.3s;
    }
    .nav a:hover {
        color: #1E90FF;
    }
    .selected {
        color: #1E90FF;
        border-bottom: 2px solid #1E90FF;
        padding-bottom: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Top Navigation ---
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

pages = ["Home", "Mood Detection", "Dataset Samples", "Model Info"]

# Navigation bar links
nav_links = ""
for p in pages:
    css_class = "selected" if st.session_state["page"] == p else ""
    nav_links += f'<a class="{css_class}" href="?page={p}">{p}</a>'

st.markdown(f'<div class="nav">{nav_links}</div>', unsafe_allow_html=True)

# Handle URL change (simulate click navigation)
query_params = st.query_params
if "page" in query_params:
    st.session_state["page"] = query_params["page"]


# --- PAGE 1: HOME ---
if st.session_state["page"] == "Home":
    st.title("😊 Mood Classifier Web App")
    st.write("""
    Welcome to the **Mood Classification Web App!**

    This app uses a deep learning model to predict whether a person appears **Happy 😄**
    or **Not Happy 😐** based on an image.

    ### 🌟 Features:
    - Upload or capture an image and predict the mood  
    - View your prediction history  
    - Explore example images from your dataset  
    - Manage model weights easily  

    Use the top navigation bar to switch between sections.
    """)


# --- PAGE 2: MOOD DETECTION ---
elif st.session_state["page"] == "Mood Detection":
    st.title("📷 Mood Detection")

    input_method = st.radio("Select input method:", ["Upload Image", "Use Camera"])

    image = None
    if input_method == "Upload Image":
        img_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if img_file:
            image = Image.open(img_file)
    else:
        cam_data = st.camera_input("Capture an image")
        if cam_data:
            image = Image.open(BytesIO(cam_data.getvalue()))

    if image:
        st.image(image, caption="Input Image", use_column_width=True)
        if st.button("🔮 Predict Mood"):
            label, prob = model.predict_pil(image)
            st.success(f"Prediction: **{label}** (Confidence: {prob:.2f})")

            history = st.session_state.get("history", [])
            history.insert(0, {"label": label, "prob": prob})
            st.session_state["history"] = history[:10]

    st.subheader("📊 Prediction History")
    for h in st.session_state.get("history", []):
        st.write(f"- {h['label']} — {h['prob']:.2f}")


# --- PAGE 3: DATASET SAMPLES ---
elif st.session_state["page"] == "Dataset Samples":
    st.title("🖼️ Example Dataset Images")

    samples = load_samples(TRAIN_DIR)
    if samples:
        cols = st.columns(4)
        for i, (mood, path) in enumerate(samples[:16]):
            with cols[i % 4]:
                st.image(str(path), width=150, caption=mood)
    else:
        st.warning("No dataset found! Please add images inside 'trainning/happy' and 'trainning/not happy' folders.")


# --- PAGE 4: MODEL INFO ---
elif st.session_state["page"] == "Model Info":
    st.title("⚙️ Model Information")

    if WEIGHTS_FILE.exists():
        st.success(f"✅ Model weights found: {WEIGHTS_FILE.name}")
    else:
        st.error("❌ Model weights not found!")

    uploaded_weights = st.file_uploader("Upload new weights (.h5)", type=["h5"])
    if uploaded_weights:
        with open(WEIGHTS_FILE, "wb") as f:
            f.write(uploaded_weights.read())
        st.success("✅ Weights uploaded successfully! Please reload the app.")

    if st.button("Reload Model"):
        st.session_state["model"] = MoodModel(str(WEIGHTS_FILE) if WEIGHTS_FILE.exists() else None)
        st.success("Model reloaded with current weights!")

    st.markdown("""
    **Model Description:**
    - Binary classifier (Happy vs Not Happy)
    - Uses CNN (Convolutional Neural Network)
    - Input: Face or portrait image
    - Output: Mood label + confidence score
    - Threshold: 0.5 for decision boundary
    """)

st.write("---")
st.caption("Developed with ❤️ using Streamlit | Version 2.0")
