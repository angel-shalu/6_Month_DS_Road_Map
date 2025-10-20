# Mood Classification App

This small Streamlit app wraps the CNN model from the notebook `image_classification.ipynb` and provides a simple UI to upload images or use your camera to predict whether the face is "happy" or "not happy".

Files added

- `model.py` — builds the CNN and exposes a `MoodModel` wrapper for inference
- `app.py` — Streamlit app to upload/capture images, run predictions, view history and sample images
- `requirements.txt` — Python dependencies

How to run (Windows PowerShell)

1. Create and activate a Python virtual environment (recommended):

```powershell
python -m venv .venv
; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the Streamlit app:

```powershell
streamlit run app.py
```

Notes and next steps

- The notebook used an unusual rescale factor; this app uses the standard 1/255 scaling for images.
- If you have trained weights saved as `mood_weights.h5` in the same folder, the app will load them automatically. You can also upload a weights file from the sidebar.
- Features added: webcam input, prediction history (in-session), sample image preview, ability to upload and save weights.
- Improvements you may want: add a training script to save weights from your dataset, improve the UI, or export predictions to CSV.
