from flask import Flask, render_template, request
import pyttsx3
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

app = Flask(__name__)

def get_meanings(word):
    synsets = wordnet.synsets(word)
    meanings = [syn.definition() for syn in synsets]
    return meanings

def get_synonyms(word):
    syn_words = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            syn_words.add(lemma.name())
    return list(syn_words)

def get_antonyms(word):
    ant_words = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                ant_words.add(lemma.antonyms()[0].name())
    return list(ant_words)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        word = request.form['word']
        meanings = get_meanings(word)
        synonyms = get_synonyms(word)
        antonyms = get_antonyms(word)
        result = {
            'word': word,
            'meanings': meanings,
            'synonyms': synonyms,
            'antonyms': antonyms
        }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
