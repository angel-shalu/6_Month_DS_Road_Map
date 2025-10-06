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
