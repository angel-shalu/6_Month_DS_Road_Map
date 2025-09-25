
import streamlit as st
from gtts import gTTS
from gtts.lang import tts_langs
import numpy as np
import os

# 📘 Get all supported languages as a dictionary: {'en': 'English', 'hi': 'Hindi', ...}
languages = tts_langs()

# 🧾 Create dropdown-friendly list like: ['English (en)', 'Hindi (hi)', ...]
language_options = [f"{name} ({code})" for code, name in languages.items()]

# 🌟 Streamlit App Title
st.markdown("<h1 style='color:#4b8bff;'>🗣️ Text-to-Speech App</h1>", unsafe_allow_html=True)
st.markdown("Convert your text into spoken words using Google Text-to-Speech.")
st.markdown("---")

# 📝 Text input
user_text = st.text_area("✏️ Enter the text to convert to speech:", height=150)



# 🌍 Language and Voice selector in sidebar navigation panel
st.sidebar.markdown("## 🌐 Language Selection")
selected_lang = st.sidebar.selectbox("Choose a language", options=language_options)

st.sidebar.markdown("## 🗣️ Voice Type")
voice_type = st.sidebar.selectbox(
    "Choose a voice type",
    ["Default (Female)", "Male", "Kids"]
)

# Extract code from selection (e.g., 'English (en)' → 'en')
lang_code = selected_lang.split("(")[-1].replace(")", "").strip()

# 🎤 Convert and play
if st.button("🔊 Convert and Play"):
    if user_text.strip() == "":
        st.warning("Please enter some text to convert.")
    elif voice_type != "Default (Female)":
        st.warning(f"The selected voice type ('{voice_type}') is not supported with the current engine. Only the default (female) voice is available.")
    else:
        tts = gTTS(text=user_text, lang=lang_code)
        file_path = "tts_output.mp3"
        tts.save(file_path)

        # Play audio
        with open(file_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

        st.success(f"✅ Speech generated in {selected_lang}!")
