import streamlit as st
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize, wordpunct_tokenize, WhitespaceTokenizer
from nltk.util import ngrams, bigrams, trigrams
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Download resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

st.title("🔤 NLP Playground: Explore Tokenization, Roots & Embeddings")

# Sidebar navigation
st.sidebar.title("Navigation")
tokenizer_option = st.sidebar.radio(
    "Choose a tokenizer:",
    ("Word Tokenizer", "Sentence Tokenizer", "WordPunct Tokenizer", "Whitespace Tokenizer")
)

st.sidebar.markdown("---")
generate_ngrams = st.sidebar.checkbox("Generate N-grams")
if generate_ngrams:
    n_val = st.sidebar.selectbox(
        "Choose N-gram type:",
        options=[2, 3, 4, 5],
        index=0,
        format_func=lambda x: f"{x}-gram"
    )


apply_stemming = st.sidebar.checkbox("Apply Stemming")
apply_lemmatization = st.sidebar.checkbox("Apply Lemmatization")
apply_stopwords = st.sidebar.checkbox("Remove Stopwords")
apply_pos = st.sidebar.checkbox("Show POS Tags")

st.sidebar.markdown("---")
embedding_option = st.sidebar.multiselect(
    "Choose the Embedding Techniques:",
    ["Bag-of-Words", "TF-IDF", "Word2Vec"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("📚 Libraries Used")
st.sidebar.markdown("""
*NLTK*: Tokenization, stemming, lemmatization, POS tagging, stopwords, n-grams.  
*Pandas*: Comparison tables.  
*Scikit-learn*: Bag-of-Words & TF-IDF embeddings.  
*Streamlit*: Interactive web app.
""")

# Main area
sentence = st.text_area("Enter a sentence:", '''Artificial Intelligence refers to the intelligence of machines. 
This is in contrast to the natural intelligence of humans and animals. 
With Artificial Intelligence, machines perform functions such as learning, planning, reasoning and problem-solving. 
Most noteworthy, Artificial Intelligence is the simulation of human intelligence by machines. 
It is probably the fastest-growing development in the World of technology and innovation. 
Furthermore, many experts believe AI could solve major challenges and crisis situations.''')

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

    # Stopword removal
    if apply_stopwords:
        stop_words = set(stopwords.words("english"))
        tokens = [w for w in tokens if w.lower() not in stop_words]

    # Display tokens
    st.subheader("✅ Tokens:")
    st.write(tokens)
    st.info(f"Total tokens: {len(tokens)}")

    # POS tagging
    if apply_pos:
        pos_tags = nltk.pos_tag(tokens)
        st.subheader("🧩 POS Tags")
        
        # Convert to DataFrame for cleaner display
        pos_df = pd.DataFrame(pos_tags, columns=["Word", "POS Tag"])
        st.dataframe(pos_df, use_container_width=True)

        # Show unique POS categories used
        unique_pos = pos_df["POS Tag"].unique()
        st.markdown("**Parts of Speech used in this text:**")
        st.write(", ".join(unique_pos))


    # Word frequency
    st.subheader("📊 Word Frequency")
    freq = Counter(tokens)
    freq_df = pd.DataFrame(freq.items(), columns=["Word", "Count"]).sort_values(by="Count", ascending=False)
    st.dataframe(freq_df, use_container_width=True)

    # Generate N-grams
    if generate_ngrams:
        st.subheader("🔗 N-grams Explorer")

        # Let user pick which grams to show
        gram_choice = st.radio(
            "Choose which n-grams to display:",
            options=["Selected N-grams", "Bigrams", "Trigrams", "All"],
            horizontal=True
        )

        # Show selected n-grams
        if gram_choice == "Selected N-grams":
            ngram_list = list(ngrams(tokens, n_val))
            st.markdown(f"**{n_val}-grams:**")
            st.write(ngram_list)
            st.info(f"Total {n_val}-grams: {len(ngram_list)}")

        elif gram_choice == "Bigrams":
            bigram_list = list(bigrams(tokens))
            st.markdown("**📍 Bigrams**")
            st.write(bigram_list)
            st.info(f"Total Bigrams: {len(bigram_list)}")

        elif gram_choice == "Trigrams":
            trigram_list = list(trigrams(tokens))
            st.markdown("**📍 Trigrams**")
            st.write(trigram_list)
            st.info(f"Total Trigrams: {len(trigram_list)}")

        elif gram_choice == "All":
            # Selected n
            ngram_list = list(ngrams(tokens, n_val))
            st.markdown(f"**{n_val}-grams:**")
            st.write(ngram_list)

            # Bigrams
            bigram_list = list(bigrams(tokens))
            st.markdown("**📍 Bigrams**")
            st.write(bigram_list)

            # Trigrams
            trigram_list = list(trigrams(tokens))
            st.markdown("**📍 Trigrams**")
            st.write(trigram_list)


    # 🔹 Stemming (separate section)
    if apply_stemming:
        st.subheader("🌱 Stemming Results")
        porter = PorterStemmer()
        lancaster = LancasterStemmer()
        snowball = SnowballStemmer("english")

        stem_data = {
            "Token": tokens,
            "Porter Stemmer": [porter.stem(w) for w in tokens],
            "Lancaster Stemmer": [lancaster.stem(w) for w in tokens],
            "Snowball Stemmer": [snowball.stem(w) for w in tokens],
        }
        stem_df = pd.DataFrame(stem_data)
        st.dataframe(stem_df, use_container_width=True)

    # 🔹 Lemmatization (separate section)
    if apply_lemmatization:
        st.subheader("📖 Lemmatization Results")
        lemmatizer = WordNetLemmatizer()
        
        lemma_data = {
            "Token": tokens,
            "Lemmatizer": [lemmatizer.lemmatize(w) for w in tokens],
        }
        lemma_df = pd.DataFrame(lemma_data)
        st.dataframe(lemma_df, use_container_width=True)


    # Embedding Techniques
    if embedding_option:
        st.subheader("📦 Embedding Representations")

        if "Bag-of-Words" in embedding_option:
            vectorizer = CountVectorizer()
            bow_matrix = vectorizer.fit_transform([sentence])
            bow_df = pd.DataFrame(bow_matrix.toarray(), columns=vectorizer.get_feature_names_out())
            st.markdown("**Bag-of-Words (BoW)**")
            st.dataframe(bow_df, use_container_width=True)

        if "TF-IDF" in embedding_option:
            tfidf = TfidfVectorizer()
            tfidf_matrix = tfidf.fit_transform([sentence])
            tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out())
            st.markdown("**TF-IDF Representation**")
            st.dataframe(tfidf_df, use_container_width=True)
