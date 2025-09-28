# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 14:29:59 2025

@author: shali
"""

import numpy as np
import pandas as pd
import re
import nltk
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# ============================
# 1. Load dataset
# ============================
dataset = pd.read_csv(
    r"C:\Users\shali\Desktop\DS_Road_Map\9. NLP\NLP_Project\CUSTOMERS REVIEW\Restaurant_Reviews_dummy.tsv",
    delimiter="\t", quoting=3
)

dataset.dropna(inplace=True)
dataset.reset_index(drop=True, inplace=True)  # reset index after dropna

# ============================
# 2. Preprocessing
# ============================
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

corpus = []
ps = PorterStemmer()

for i in range(len(dataset)):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'].iloc[i])  # use .iloc
    review = review.lower().split()
    review = [ps.stem(word) for word in review]   # keep stopwords
    corpus.append(' '.join(review))

# ============================
# Target column cleanup
# ============================
y = dataset.iloc[:, 1].astype(str).str.strip()

# Map to numeric (force only 0 and 1, drop invalid labels like "Liked")
y = y.replace({'0': 0, '1': 1, 'Liked': 1})  # treat "Liked" as 1 (positive)
y = pd.to_numeric(y, errors='coerce')        # convert to numeric
dataset = dataset.loc[y.notna()]             # drop rows with invalid labels
y = y.dropna().astype(int).values            # final numeric labels

# ============================
# 3. Vectorizer (TF-IDF)
# ============================
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizers = {"TF-IDF": TfidfVectorizer(max_features=1500)}

# ============================
# 4. Classifiers
# ============================
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

# ============================
# 5. Train/Test Split & Evaluation
# ============================
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score

results = []

for vec_name, vec in vectorizers.items():
    x = vec.fit_transform(corpus).toarray()
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    for clf_name, clf in classifiers.items():
        clf.fit(x_train, y_train)

        # Predictions
        y_pred = clf.predict(x_test)
        y_train_pred = clf.predict(x_train)

        # Metrics
        acc = accuracy_score(y_test, y_pred)
        bias = accuracy_score(y_train, y_train_pred)  # Train acc
        variance = accuracy_score(y_test, y_pred)     # Test acc

        # AUC (binary only)
        auc = None
        try:
            if hasattr(clf, "predict_proba"):
                y_prob = clf.predict_proba(x_test)[:, 1]
                auc = roc_auc_score(y_test, y_prob)
            elif hasattr(clf, "decision_function"):
                y_score = clf.decision_function(x_test)
                auc = roc_auc_score(y_test, y_score)
        except:
            auc = None

        # Store results
        results.append({
            "Vectorizer": vec_name,
            "Model": clf_name,
            "Accuracy": acc,
            "Bias": bias,
            "Variance": variance,
            "AUC": auc,
            "ConfusionMatrix": confusion_matrix(y_test, y_pred)
        })

# ============================
# 6. Print Results
# ============================
for r in results:
    print(f"--- {r['Vectorizer']} | {r['Model']} ---")
    print(f"Accuracy: {r['Accuracy']:.3f}, Bias: {r['Bias']:.3f}, Variance: {r['Variance']:.3f}, AUC: {r['AUC']}")
    print(r["ConfusionMatrix"])
    print()


# ============================
# 7. Best Fit Model Selection
# ============================

best_model = None
best_score = -1

for r in results:
    # closeness = how close train (bias) and test (variance) are
    closeness = 1 - abs(r["Bias"] - r["Variance"])  
    
    # final score balances accuracy and closeness
    score = (r["Accuracy"] + closeness) / 2  
    
    if score > best_score:
        best_score = score
        best_model = r

print("✅ Best Fit Model Selected")
print(f"Model: {best_model['Model']} | Vectorizer: {best_model['Vectorizer']}")
print(f"Accuracy: {best_model['Accuracy']:.3f}")
print(f"Bias (Train Acc): {best_model['Bias']:.3f}")
print(f"Variance (Test Acc): {best_model['Variance']:.3f}")
print(f"AUC: {best_model['AUC']}")
print("Confusion Matrix:")
print(best_model["ConfusionMatrix"])


# ============================
# 8. Visualization
# ============================
import seaborn as sns

# Convert results list to DataFrame
df_results = pd.DataFrame(results)

# --- Plot Accuracy comparison ---
plt.figure(figsize=(10, 6))
sns.barplot(x="Model", y="Accuracy", hue="Vectorizer", data=df_results)
plt.title("Model Accuracy Comparison")
plt.xticks(rotation=45)
plt.ylim(0, 1)
plt.tight_layout()
plt.show()

# --- Plot Bias vs Variance (Train vs Test Accuracy) ---
plt.figure(figsize=(10, 6))
df_results_melt = df_results.melt(
    id_vars=["Model", "Vectorizer"], 
    value_vars=["Bias", "Variance"], 
    var_name="Type", 
    value_name="Score"
)
sns.barplot(x="Model", y="Score", hue="Type", data=df_results_melt)
plt.title("Bias (Train Acc) vs Variance (Test Acc)")
plt.xticks(rotation=45)
plt.ylim(0, 1)
plt.tight_layout()
plt.show()

# --- Plot AUC comparison (if available) ---
if df_results["AUC"].notna().any():
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Model", y="AUC", hue="Vectorizer", data=df_results)
    plt.title("Model AUC Comparison")
    plt.xticks(rotation=45)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()

