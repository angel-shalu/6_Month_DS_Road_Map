
# XML scrapping for xml sheet 

import os
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup

# Change working directory
os.chdir(r"C:\Users\shali\Desktop\DS_Road_Map\9. NLP\NLP WEB SCRAPING\xml_single articles")

# Parse XML file
tree = ET.parse("769952.xml") 
root = tree.getroot()

# Convert XML root to string
root = ET.tostring(root, encoding='utf8').decode('utf8')

# Functions
def strip_html(text):
    soup = BeautifulSoup(text, "xml")   # use XML parser
    return soup.get_text()

def remove_between_square_brackets(text):
    return re.sub(r'\[[^]]*\]', '', text)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    text = re.sub('  +', ' ', text)  # remove extra spaces
    return text.strip()

# Clean text
sample = denoise_text(root)

# ✅ Save cleaned text into UTF-8 file
output_file = "cleaned_text.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(sample)

print(f"Cleaned text saved to {output_file}")
