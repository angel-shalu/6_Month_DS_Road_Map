import streamlit as st
import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB

# Optional classifiers
try:
    from xgboost import XGBClassifier
    xgb_available = True
except:
    xgb_available = False
try:
    from lightgbm import LGBMClassifier
    lgbm_available = True
except:
    lgbm_available = False
    
# Load dataset
DATA_PATH = r"Restaurant_Reviews_dummy.tsv"
dataset = pd.read_csv(DATA_PATH, delimiter="\t", quoting=3)

# Drop rows with missing Review or Label
dataset = dataset.dropna(subset=['Review', dataset.columns[1]])
dataset.reset_index(drop=True, inplace=True)

# Preprocessing
ps = PorterStemmer()
def preprocess_review(review):
    review = re.sub('[^a-zA-Z]', ' ', str(review))  # ensure string
    review = review.lower().split()
    review = [ps.stem(word) for word in review]
    return ' '.join(review)

corpus = [preprocess_review(text) for text in dataset['Review']]

# ---- FIX FOR y ----
# Clean label column
y = dataset.iloc[:, 1].astype(str).str.strip()
y = y.replace({'0': 0, '1': 1, 'Liked': 1})   # map labels
y = pd.to_numeric(y, errors='coerce')         # force numeric
dataset = dataset.loc[y.notna()]              # drop invalid rows
y = y.dropna().astype(int).values             # final numpy int labels



# Sidebar: Vectorizer selection
st.sidebar.title("Navigation")
vectorizer_type = st.sidebar.radio("Select vectorizer:", ["TF-IDF", "CountVectorizer"])
if vectorizer_type == "TF-IDF":
    vectorizer = TfidfVectorizer(max_features=1500)
else:
    vectorizer = CountVectorizer(max_features=1500)
x = vectorizer.fit_transform(corpus).toarray()

# Classifiers
def get_classifiers():
    classifiers = {
        "LogisticRegression": LogisticRegression(max_iter=500, random_state=0),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=0),
        "DecisionTree": DecisionTreeClassifier(random_state=0),
        "SVM": SVC(probability=True, random_state=0),
        "NaiveBayes": MultinomialNB()
    }
    if xgb_available:
        classifiers["XGBoost"] = XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=0)
    if lgbm_available:
        classifiers["LightGBM"] = LGBMClassifier(random_state=0)
    return classifiers

# Train all classifiers (for demo, quick train)
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


classifiers = get_classifiers()
metrics = {}
for name, clf in classifiers.items():
    clf.fit(x_train, y_train)
    y_train_pred = clf.predict(x_train)
    y_test_pred = clf.predict(x_test)
    acc = (y_test == y_test_pred).mean()
    bias = (y_train == y_train_pred).mean()
    variance = acc  # For this context, variance is test accuracy
    metrics[name] = {
        "Accuracy": acc,
        "Bias": bias,
        "Variance": variance
    }

# Streamlit UI
st.set_page_config(page_title="Restaurant Review Sentiment App", page_icon="🍽️", layout="centered")
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🍽️ Restaurant Review Sentiment App")
st.write("""
Welcome! This app predicts whether a restaurant review is **positive** or **negative** using various machine learning models. 

**Instructions:**
1. Select a classifier from the sidebar.
2. Enter your restaurant review in the text box below.
3. Click **Predict** to see the result.
""")



classifier_name = st.sidebar.radio("Select classifier:", list(classifiers.keys()))
st.sidebar.info("Choose a model to use for prediction.")

# Show metrics for selected classifier and vectorizer
st.sidebar.markdown("---")
st.sidebar.subheader(f"Metrics for {classifier_name} ({vectorizer_type})")
st.sidebar.metric("Accuracy", f"{metrics[classifier_name]['Accuracy']:.2f}")
st.sidebar.metric("Bias (Train Acc)", f"{metrics[classifier_name]['Bias']:.2f}")
st.sidebar.metric("Variance (Test Acc)", f"{metrics[classifier_name]['Variance']:.2f}")

st.markdown("---")
user_review = st.text_area("Enter your restaurant review here:", height=120)

col1, col2 = st.columns([1,2])
with col1:
    predict_btn = st.button("Predict", use_container_width=True)

if predict_btn:
    if user_review.strip() == "":
        st.warning("Please enter a review.")
    else:
        processed = preprocess_review(user_review)
        vect = vectorizer.transform([processed]).toarray()
        clf = classifiers[classifier_name]
        pred = clf.predict(vect)[0]
        prob = clf.predict_proba(vect)[0][1] if hasattr(clf, "predict_proba") else None
        label = "🟢 Positive" if pred == 1 else "🔴 Negative"
        st.success(f"**Prediction:** {label}")
        if prob is not None:
            st.info(f"**Probability (positive):** {prob:.2f}")
