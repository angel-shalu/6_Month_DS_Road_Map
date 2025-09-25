
import streamlit as st
import spacy

# Load spaCy model (change to your model if needed)
@st.cache_resource
def load_model():
    return spacy.load('en_core_web_sm')
nlp = load_model()

def summarize_text(text, max_sent_len=100, min_ratio=0.1):
    doc = nlp(text)
    sentences = list(doc.sents)
    ranked = sorted(sentences, key=lambda sent: len([ent for ent in sent.ents]), reverse=True)
    # Take top 3 sentences as summary (customize as needed)
    summary_sents = [sent.text for sent in ranked[:3]]
    # Filter by max sentence length
    summary_sents = [s for s in summary_sents if len(s.split()) <= max_sent_len]
    summary = ' '.join(summary_sents)
    # Enforce min ratio
    orig_len = len(text.split())
    summ_len = len(summary.split())
    ratio_actual = (summ_len / orig_len) if orig_len else 0
    if ratio_actual < min_ratio and orig_len > 0:
        # Add more sentences if possible
        for sent in ranked[3:]:
            if len(sent.text.split()) <= max_sent_len:
                summary_sents.append(sent.text)
                summary = ' '.join(summary_sents)
                summ_len = len(summary.split())
                ratio_actual = (summ_len / orig_len)
                if ratio_actual >= min_ratio:
                    break
    return summary, orig_len, summ_len, ratio_actual

st.set_page_config(page_title="Text Summarizer", page_icon="📝", layout="wide")

# Sidebar navigation panel
st.sidebar.header("Navigation & Settings")
max_sent_len = st.sidebar.number_input("Max Sentence Length (words)", 1, 50, 10, step=1)
min_sent_len = st.sidebar.number_input("Min Sentence Length (words)", 1, 50, 1, step=1)
min_ratio = st.sidebar.slider("Length of Summary/Original Ratio", 0.05, 1.0, 0.1, 0.01)
st.sidebar.markdown(f"**Current Settings:**\n- Max Sentence Length: {max_sent_len} \n- Min Sentence Length: {min_sent_len}\n- Ratio Rate: {min_ratio}")

st.title('Text Summarization App')

# Input method selection
input_method = st.radio("Choose Input Method:", ["Enter Text", "Upload File", "Paste Test"])
input_text = ""
if input_method == "Enter Text":
    input_text = st.text_area('Enter text to summarize:', height=200)
elif input_method == "Upload File":
    uploaded_file = st.file_uploader("Upload a .txt, .pdf, or .docx file", type=["txt", "pdf", "docx"])
    if uploaded_file:
        input_text = uploaded_file.read().decode("utf-8")
elif input_method == "Paste Test":
    input_text = st.text_area('Paste your test case here:', height=200)

if st.button('Summarize'):
    if input_text.strip():
        summary, orig_len, summ_len, ratio_actual = summarize_text(input_text, max_sent_len, min_ratio)
        st.subheader('Summary:')
        st.write(summary)
        st.info(f"Summary length: {summ_len} words | Original: {orig_len} words | Ratio: {ratio_actual:.2f}")
        if summ_len > 0 and ratio_actual < min_ratio:
            st.warning(f"Summary is shorter than the minimum ratio ({min_ratio}).")
        if any(len(sent.split()) > max_sent_len for sent in summary.split('.')):
            st.warning(f"Some summary sentences exceed the maximum sentence length of {max_sent_len} words.")
    else:
        st.warning('Please enter some text or upload a file.')
