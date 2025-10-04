import streamlit as st
from mtranslate import translate
import pandas as pd
import os
from gtts import gTTS
import base64

# read language dataset
df = pd.read_csv(r"C:\Users\shali\Desktop\DS_Road_Map\9. NLP\NLP_Project\MULTIPLE LANGUAGE TRANSLATION\language.csv")
df.dropna(inplace=True)
lang = df['name'].to_list()
langlist=tuple(lang)
langcode = df['iso'].to_list()

# create dictionary of language and 2 letter langcode
lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}


# --- Custom Page Config and Style ---
st.set_page_config(page_title="🌐 Language Translator", page_icon="🌍", layout="centered")
st.markdown("""
<style>
.main {background-color: #f8f9fa;}
.stButton>button {background-color: #4CAF50; color: white; font-weight: bold;}
.stTextArea textarea {font-size: 1.1em;}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
# 🌍 Language Translator
Easily translate text into multiple languages and listen to the result!
""")

# --- Sidebar ---
st.sidebar.header("Translation Settings")
choice = st.sidebar.selectbox('Select Target Language', langlist)
st.sidebar.markdown(f"**Language code:** `{lang_array[choice]}`")
st.sidebar.info("Choose your target language for translation. Audio is available for many languages.")

# --- Input ---

inputtext = st.text_area("Enter text to translate:", height=100, placeholder="Type or paste your text here...")
translate_btn = st.button("Enter", help="Click to translate and hear the audio.")

# --- Session State for History ---
if 'history' not in st.session_state:
    st.session_state['history'] = []

speech_langs = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "od" : "odia",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "la": "Latin",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Filipino",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-CN": "Chinese"
}

# function to decode audio file for download
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href


# --- Main Translation Logic ---
col1, col2 = st.columns([4,3])
if translate_btn and len(inputtext.strip()) > 0:
    try:
        output = translate(inputtext, lang_array[choice])
        st.session_state['history'].append((inputtext, output, choice))
        with col1:
            st.text_area("Translated Text", output, height=200, key="translated_text")
            st.button("Copy Translation", on_click=lambda: st.write("Copied!"), help="Copy translated text to clipboard.")
        # Audio support (always available, fallback to English if not supported)
        with col2:
            speech_code = lang_array[choice] if lang_array[choice] in speech_langs else 'en'
            aud_file = gTTS(text=output, lang=speech_code, slow=False)
            aud_file.save("lang.mp3")
            audio_file_read = open('lang.mp3', 'rb')
            audio_bytes = audio_file_read.read()
            st.audio(audio_bytes, format='audio/mp3')
            st.markdown(get_binary_file_downloader_html("lang.mp3", 'Audio File'), unsafe_allow_html=True)
            if lang_array[choice] not in speech_langs:
                st.caption("Audio is provided in English as the selected language is not supported for speech.")
    except Exception as e:
        st.error(f"Translation failed: {e}")

# --- Translation History ---
if st.session_state['history']:
    st.markdown("---")
    st.subheader("Translation History (this session)")
    for idx, (src, tgt, langname) in enumerate(reversed(st.session_state['history'][-5:]), 1):
        st.markdown(f"**{idx}.** `{src}` → `{tgt}`  ")
        st.caption(f"Language: {langname}")
