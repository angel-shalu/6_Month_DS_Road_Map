import streamlit as st
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize, wordpunct_tokenize, WhitespaceTokenizer
from nltk.util import ngrams
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer, WordNetLemmatizer

# Download punkt + wordnet if not already available
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

st.title("🔤 NLP App: Tokenizer, N-grams, Stemmer & Lemmatizer")

# User input
sentence = st.text_area("Enter a sentence:", "Artificial Intelligence refers to the intelligence of machines.")

# Tokenization options
tokenizer_option = st.radio(
    "Choose a tokenizer:",
    ("Word Tokenizer", "Sentence Tokenizer", "WordPunct Tokenizer", "Whitespace Tokenizer")
)

# N-gram settings
generate_ngrams = st.checkbox("Generate N-grams")
if generate_ngrams:
    n_val = st.slider("Select N for N-grams", min_value=2, max_value=5, value=2)

# Stemming & Lemmatization options
apply_stemming = st.checkbox("Apply Stemming")
apply_lemmatization = st.checkbox("Apply Lemmatization")

if st.button("Process"):
    # Select tokenizer
    if tokenizer_option == "Word Tokenizer":
        tokens = word_tokenize(sentence)
    elif tokenizer_option == "Sentence Tokenizer":
        tokens = sent_tokenize(sentence)
    elif tokenizer_option == "WordPunct Tokenizer":
        tokens = wordpunct_tokenize(sentence)
    elif tokenizer_option == "Whitespace Tokenizer":
        tokens = WhitespaceTokenizer().tokenize(sentence)

    # Display tokens
    st.subheader("✅ Tokens:")
    st.write(tokens)
    st.info(f"Total tokens: {len(tokens)}")

    # Generate N-grams
    if generate_ngrams:
        st.subheader(f"🔗 {n_val}-grams")
        ngram_list = list(ngrams(tokens, n_val))
        st.write(ngram_list)
        st.info(f"Total {n_val}-grams: {len(ngram_list)}")

        # Show bigrams and trigrams separately
        if n_val != 2:
            bigrams = list(ngrams(tokens, 2))
            st.subheader("📍 Bigrams")
            st.write(bigrams)

        if n_val != 3:
            trigrams = list(ngrams(tokens, 3))
            st.subheader("📍 Trigrams")
            st.write(trigrams)

    # Apply stemming and lemmatization with side-by-side comparison
    if apply_stemming or apply_lemmatization:
        st.subheader("📊 Token Comparison Table")

        # Initialize stemmers & lemmatizer
        porter = PorterStemmer()
        lancaster = LancasterStemmer()
        snowball = SnowballStemmer("english")
        lemmatizer = WordNetLemmatizer()

        # Build comparison dictionary
        data = {
            "Token": tokens
        }
        if apply_stemming:
            data["Porter Stemmer"] = [porter.stem(w) for w in tokens]
            data["Lancaster Stemmer"] = [lancaster.stem(w) for w in tokens]
            data["Snowball Stemmer"] = [snowball.stem(w) for w in tokens]
        if apply_lemmatization:
            data["Lemmatizer"] = [lemmatizer.lemmatize(w) for w in tokens]

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)