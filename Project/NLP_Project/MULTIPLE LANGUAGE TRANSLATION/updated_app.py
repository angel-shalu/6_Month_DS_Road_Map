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
body, .main {
    background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%) !important;
}
.stApp {
    background: linear-gradient(120deg, #f8fafc 0%, #e0e7ff 100%) !important;
}
.stButton>button {
    background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);
    color: #fff;
    font-weight: bold;
    border-radius: 8px;
    border: none;
    padding: 0.5em 2em;
    box-shadow: 0 2px 8px rgba(99,102,241,0.08);
    transition: 0.2s;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #06b6d4 0%, #6366f1 100%);
    color: #fff;
    box-shadow: 0 4px 16px rgba(6,182,212,0.12);
}
/* Chat Input Box Styling */
.stTextArea textarea {
    font-size: 1.1em;
    background: #f9fafb;  /* Light grey background */
    border-radius: 12px;   /* More rounded like chat apps */
    border: 1.5px solid #10b981; /* Nice green (WhatsApp-like) */
    padding: 10px;
    color: #111827;  /* Dark text */
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    transition: all 0.2s ease-in-out;
}

/* Hover effect */
.stTextArea textarea:hover {
    border-color: #059669;   /* Darker green */
    box-shadow: 0 3px 8px rgba(5,150,105,0.2);
}

/* Focus effect */
.stTextArea textarea:focus {
    border-color: #059669;  
    background: #ffffff;    /* Pure white when typing */
    outline: none;
    box-shadow: 0 4px 12px rgba(5,150,105,0.25);
}

/* Sidebar with gradient */
.stSidebar {
    background: linear-gradient(180deg, #4f46e5, #6366f1, #818cf8) !important;
    color: #ffffff !important;
    border-radius: 0 16px 16px 0;
    padding: 12px;
    box-shadow: 2px 0 8px rgba(0,0,0,0.15);
}

/* Sidebar text */
.stSidebar .css-1d391kg, .stSidebar .css-1v0mbdj {
    color: #ffffff !important;
    font-weight: 500;
}

/* Headings */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #4f46e5;  /* Deep Indigo */
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-weight: 700;
    letter-spacing: -0.5px;
}

/* Paragraphs & lists */
.stMarkdown p, .stMarkdown ul, .stMarkdown li {
    color: #1e293b;  /* Slate-900 */
    font-size: 1.08em;
    line-height: 1.6;
}

/* Links */
.stMarkdown a {
    color: #06b6d4 !important; /* Cyan */
    text-decoration: none;
    font-weight: 600;
}
.stMarkdown a:hover {
    text-decoration: underline;
    color: #0891b2 !important; /* Darker cyan */
}

/* Audio player */
.stAudio {
    color: #06b6d4 !important;
}

/* Captions */
.stCaption {
    color: #6366f1 !important;
    font-size: 0.95em;
    font-style: italic;
}

/* Subheaders */
.stSubheader {
    color: #06b6d4 !important;
    font-weight: 600;
    font-size: 1.15em;
}

</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div style="display:flex;align-items:center;gap:1em;margin-bottom:0.5em;">
    <span style="font-size:2.5em;">🌍</span>
    <span style="font-size:2.1em;font-weight:700;color:#6366f1;font-family:'Segoe UI',sans-serif;">Language Translator</span>
</div>
<p style="font-size:1.15em;color:#334155;">Easily translate text into multiple languages and listen to the result!</p>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.header("Translation Settings")
choice = st.sidebar.selectbox('Select Target Language', langlist)
st.sidebar.markdown(f"**Language code:** `{lang_array[choice]}`")
st.sidebar.info("Choose your target language for translation. Audio is available for many languages.")

# --- Input ---

inputtext = st.text_area("Enter text to translate:", height=200, placeholder="Type or paste your text here...")
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
