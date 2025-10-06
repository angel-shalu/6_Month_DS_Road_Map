# XML scrapping for xml sheet 

import os
os.chdir(r"C:\Users\shali\Desktop\DS_Road_Map\9. NLP\NLP WEB SCRAPING\xml_single articles")

import xml.etree.ElementTree as ET

tree = ET.parse("769952.xml") 
root = tree.getroot()

root=ET.tostring(root, encoding='utf8').decode('utf8')

root

import re, string, unicodedata
import nltk

from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

def strip_html(text):
    soup = BeautifulSoup(text, "xml")
    return soup.get_text()

def remove_between_square_brackets(text):
    return re.sub(r'\[[^]]*\]', '', text)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    text=re.sub('  ','',text)
    return text

sample = denoise_text(root)
print(sample)

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Sample text
sample = """
Natural Language Processing (NLP) is a field of Artificial Intelligence 
that focuses on the interaction between humans and computers using natural language.
"""

# --- Tokenization ---
# Word tokens
word_tokens = word_tokenize(sample)
print("Word Tokens:\n", word_tokens)

# Sentence tokens
sent_tokens = sent_tokenize(sample)
print("\nSentence Tokens:\n", sent_tokens)

# --- Stopwords ---
stop_words = set(stopwords.words('english'))
filtered_words = [w for w in word_tokens if w.lower() not in stop_words]
print("\nFiltered Words (Stopwords removed):\n", filtered_words)

# --- Stemming ---
ps = PorterStemmer()
stemmed_words = [ps.stem(w) for w in filtered_words]
print("\nStemmed Words:\n", stemmed_words)

# --- POS Tagging ---
pos_tags = pos_tag(word_tokens)
print("\nPOS Tags:\n", pos_tags)

# --- WordCloud ---
text_for_wc = " ".join(filtered_words)
wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text_for_wc)

# Display the WordCloud
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()