import streamlit as st
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize, wordpunct_tokenize, WhitespaceTokenizer
from nltk.util import ngrams
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer, WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Custom CSS for sidebar and main area
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: bold;
        color: #4F8BF9;
        text-align: center;
        margin-bottom: 0.5em;
        letter-spacing: 1px;
    }
    /* Change sidebar background color and style */
    section[data-testid="stSidebar"] {
        background: linear-gradient(120deg, #1CB5E0 0%, #4F8BF9 100%) !important;
        border-radius: 0 18px 18px 0;
        box-shadow: 2px 0 8px rgba(79,139,249,0.08);
        color: #fff !important;
    }
    /* Sidebar text color */
    section[data-testid="stSidebar"] .css-1v0mbdj, /* radio/checkbox label */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .css-1cpxqw2 {
        color: #fff !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4F8BF9 0%, #1CB5E0 100%);
        color: white;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 0.5em 2em;
        margin-top: 1em;
    }
    .stDataFrame, .stTable {
        background: #fff;
        border-radius: 10px;
        box-shadow: 0 1px 4px rgba(79,139,249,0.07);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🔤 NLP App: Tokenizer, N-grams, Stemmer & Lemmatizer</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
tokenizer_option = st.sidebar.radio(
    "Select Tokenization Method:",
    ("Word Tokenizer", "Sentence Tokenizer", "WordPunct Tokenizer", "Whitespace Tokenizer")
)

st.sidebar.markdown("---")
generate_ngrams = st.sidebar.checkbox("Generate N-grams")
if generate_ngrams:
    n_val = st.sidebar.slider("Select N for N-grams", min_value=2, max_value=5, value=2)

apply_stemming = st.sidebar.checkbox("Apply Stemming")
apply_lemmatization = st.sidebar.checkbox("Apply Lemmatization")

# Main area
sentence = st.text_area("Enter a sentence:", "Artificial Intelligence refers to the intelligence of machines.")

if st.button("Process"):
    if tokenizer_option == "Word Tokenizer":
        tokens = word_tokenize(sentence)
    elif tokenizer_option == "Sentence Tokenizer":
        tokens = sent_tokenize(sentence)
    elif tokenizer_option == "WordPunct Tokenizer":
        tokens = wordpunct_tokenize(sentence)
    elif tokenizer_option == "Whitespace Tokenizer":
        tokens = WhitespaceTokenizer().tokenize(sentence)

    st.subheader("✅ Tokens:")
    st.write(tokens)
    st.info(f"Total tokens: {len(tokens)}")

    if generate_ngrams:
        st.subheader(f"🔗 {n_val}-grams")
        ngram_list = list(ngrams(tokens, n_val))
        st.write(ngram_list)
        st.info(f"Total {n_val}-grams: {len(ngram_list)}")
        if n_val != 2:
            bigrams = list(ngrams(tokens, 2))
            st.subheader("📍 Bigrams")
            st.write(bigrams)
        if n_val != 3:
            trigrams = list(ngrams(tokens, 3))
            st.subheader("📍 Trigrams")
            st.write(trigrams)

    if apply_stemming or apply_lemmatization:
        st.subheader("📊 Token Comparison Table")
        porter = PorterStemmer()
        lancaster = LancasterStemmer()
        snowball = SnowballStemmer("english")
        lemmatizer = WordNetLemmatizer()
        data = {"Token": tokens}
        if apply_stemming:
            data["Porter Stemmer"] = [porter.stem(w) for w in tokens]
            data["Lancaster Stemmer"] = [lancaster.stem(w) for w in tokens]
            data["Snowball Stemmer"] = [snowball.stem(w) for w in tokens]
        if apply_lemmatization:
            data["Lemmatizer"] = [lemmatizer.lemmatize(w) for w in tokens]
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
