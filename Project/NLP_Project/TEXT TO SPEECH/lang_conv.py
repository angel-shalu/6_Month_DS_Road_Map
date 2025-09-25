import streamlit as st
from googletrans import Translator, LANGUAGES

# Set page title and configuration
st.set_page_config(page_title="Language Converter")

# Apply custom CSS using st.markdown()
st.markdown(
    """
    <style>
    /* Add custom CSS here */
    .title {
        width: 65%;
        color: red;
        text-align: center;
        padding: 20px;
        font-weight: bold;
        background-color: yellow;
        border-radius: 10px;
        box-shadow: 2px 2px 2px 0px rgba(0,0,0,0.1);
    }
    .text {
        font-size: 1.4em;
        color: #333333;
    }
    .stButton>button {
        background-color: #4777f5;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        font-size: 1em;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Render styled elements
st.markdown('<h1 class="title">Language Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="text">This is a Language Converter UI. You can change it to your preferred language.</p>', unsafe_allow_html=True)

# Initialize the translator
translator = Translator()

st.audio("ad.m4a", format="audio/mepg", loop=False)
st.title("Language Converter")

# Text input for the text to be translated
text_to_translate = st.text_area("Hi, Please enter text here to translate")

# Dropdown for selecting source and target languages
source_language = st.selectbox("Select your source language", list(LANGUAGES.values()), index=list(LANGUAGES.keys()).index("en"))
target_language = st.selectbox("Select the target language you want", list(LANGUAGES.values()), index=list(LANGUAGES.keys()).index("es"))

# Find language codes from language names

source_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(source_language)]
target_lang_code =  list(LANGUAGES.keys())[list(LANGUAGES.values()).index(target_language)]

# Translate button
if st.button("Translate"):
    if text_to_translate:
        translated = translator.translate(text_to_translate, src=source_lang_code, dest=target_lang_code)
        st.success("Translated Successfully !")
        st.write(translated.text)
    else:
        st.warning("Please enter some text to translate.")
