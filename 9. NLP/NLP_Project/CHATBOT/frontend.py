import streamlit as st
from nltk.chat.util import Chat, reflections

# Define pairs
pairs = [
    [
        r"(.*)my name is (.*)",
        ["Hello %2, How are you today ?",]
    ],
    [
        r"(.*)help(.*)",
        ["I can help you ",]
    ],
    [
        r"(.*) your name ?",
        ["My name is thecleverprogrammer, but you can just call me robot and I'm a chatbot .",]
    ],
    [
        r"how are you (.*) ?",
        ["I'm doing very well", "I am great !"]
    ],
    [
        r"sorry (.*)",
        ["Its alright","Its OK, never mind that",]
    ],
    [
        r"i'm (.*) (good|well|okay|ok)",
        ["Nice to hear that","Alright, great !",]
    ],
    [
        r"(hi|hey|hello|hola|holla)(.*)",
        ["Hello", "Hey there",]
    ],
    [
        r"what (.*) want ?",
        ["Make me an offer I can't refuse",]
    ],
    [
        r"(.*)created(.*)",
        ["Prakash created me using Python's NLTK library ","Top secret ;)",]
    ],
    [
        r"(.*) (location|city) ?",
        ['Hyderabad, India',]
    ],
    [
        r"(.*)raining in (.*)",
        ["No rain in the past 4 days here in %2","In %2 there is a 50% chance of rain",]
    ],
    [
        r"how (.*) health (.*)",
        ["Health is very important, but I am a computer, so I don't need to worry about my health ",]
    ],
    [
        r"(.*)(sports|game|sport)(.*)",
        ["I'm a very big fan of Cricket",]
    ],
    [
        r"who (.*) (Cricketer|Batsman)?",
        ["Virat Kohli"]
    ],
    [
        r"quit",
        ["Bye for now. See you soon :) ","It was nice talking to you. See you soon :)"]
    ],
    [
        r"(.*)",
        ['Our customer service will reach you']
    ],
]

# Create Chat object
chat = Chat(pairs, reflections)

# Streamlit UI
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 NLTK Chatbot")
st.write("Type lowercase English to start a conversation. Type **quit** to end.")

# Session state for conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# User input box
user_input = st.text_input("You:", key="input")

if user_input:
    response = chat.respond(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", response))

# Display chat history
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"🧑 **You:** {message}")
    else:
        st.markdown(f"🤖 **Bot:** {message}")
