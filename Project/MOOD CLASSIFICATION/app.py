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

# --- Helper function to load dataset samples ---
def load_samples(folder):
    samples = []
    for mood in ["happy", "not happy"]:
        mood_folder = folder / mood
        if mood_folder.exists():
            for img_path in mood_folder.glob("*.[jp][pn]g"):
                samples.append((mood, img_path))
    return samples


# --- Initialize model ---
if "model" not in st.session_state:
    st.session_state["model"] = MoodModel(str(WEIGHTS_FILE) if WEIGHTS_FILE.exists() else None)
model = st.session_state["model"]


# --- Main Streamlit App ---
def main():
    st.set_page_config(page_title="Mood Classifier", layout="wide", page_icon="😊")

    # --- Navigation Menu ---
    menu = ["🏠 Home", "📷 Mood Detection", "🖼️ Dataset Samples", "⚙️ Model Info"]
    choice = st.sidebar.radio("Navigate", menu)

    # --- HOME PAGE ---
    if choice == "🏠 Home":
        st.title("😊 Mood Classifier App")
        st.write("""
        Welcome to the **Mood Classification App**!

        This application predicts whether a person is **Happy 😄** or **Not Happy 😐** 
        from an uploaded or captured image using a deep learning model.

        **Features:**
        - Upload or take a picture and predict the mood
        - View prediction history
        - Browse example images from your dataset
        - Manage and upload model weights

        Use the sidebar to explore different sections of the app.
        """)

    # --- MOOD DETECTION PAGE ---
    elif choice == "📷 Mood Detection":
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

                # store prediction history
                history = st.session_state.get("history", [])
                history.insert(0, {"label": label, "prob": prob})
                st.session_state["history"] = history[:10]

        st.subheader("📊 Prediction History")
        for h in st.session_state.get("history", []):
            st.write(f"- {h['label']} — {h['prob']:.2f}")

    # --- DATASET SAMPLES PAGE ---
    elif choice == "🖼️ Dataset Samples":
        st.title("🖼️ Example Dataset Images")

        samples = load_samples(TRAIN_DIR)
        if samples:
            cols = st.columns(4)
            for i, (mood, path) in enumerate(samples[:16]):
                with cols[i % 4]:
                    st.image(str(path), width=150, caption=mood)
        else:
            st.warning("No dataset found! Please add sample images in 'trainning/happy' and 'trainning/not happy' folders.")
            
        
    
    # --- MODEL INFO PAGE ---
    elif choice == "⚙️ Model Info":
        st.title("⚙️ Model Information")

        if WEIGHTS_FILE.exists():
            st.success(f"✅ Model weights found: {WEIGHTS_FILE.name}")
        else:
            st.error("❌ Model weights file not found!")

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
        - Type: Binary classifier (Happy vs Not Happy)
        - Input: Face or portrait image
        - Output: Class label + confidence score
        - Threshold: 0.5 for binary decision
        """)

    # --- Footer ---
    st.write("---")
    st.caption("Developed by Shalini ❤️")


# --- Run App ---
if __name__ == "__main__":
    main()
