import streamlit as st
import requests
import time
import threading
import pyttsx3
from gtts import gTTS
import tempfile
import os

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# # Function to speak text in a separate thread
# def speak(text):
#     def run():
#         engine = pyttsx3.init()
#         engine.say(text)
#         engine.runAndWait()
#     threading.Thread(target=run, daemon=True).start()

def speak(text):
    try:
        tts = gTTS(text=text, lang="en")
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts.save(fp.name)
            os.system(f"mpg123 {fp.name}")  # Requires mpg123 package
    except Exception as e:
        st.error(f"Speech synthesis failed: {e}")

# Title and Description
st.title("🤖 BOT-ME: AI Assistant")
st.write("This chatbot can answer questions based on predefined data from a PDF.")

# Custom CSS to remove Streamlit default containers
st.markdown("""
    <style>
        /* Remove default padding and margins */
        body {
            margin: 0;
            padding: 0;
        }

        /* Remove any padding or background from Streamlit's main content */
        .css-1v3fvcr, .css-18e3th9 {
            background: transparent !important;
            padding: 0 !important;
        }

        /* Custom styling for chat container */
        .chat-container {
            max-height: 50vh;  /* Limit height for chat container */
            overflow-y: auto;  /* Enable scrolling when content overflows */
            padding: 10px;
            border-radius: 10px;
            background-color: #f9f9f9;
            display: flex;
            flex-direction: column;
            position: relative;
            width: 100%;
            overflow-x: hidden;
            margin-top: 10px;
        }

        /* Style for individual messages */
        .message {
            max-width: 70%;
            word-wrap: break-word;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            font-size: 16px;
            display: inline-block;
            color: black;  /* Set text color to black */
        }

        .user-message {
            background-color: #DCF8C6;
            text-align: right;
            align-self: flex-end;  /* Move user message to the right */
        }

        .bot-message {
            background-color: #E3E3E3;
            text-align: left;
            align-self: flex-start;  /* Keep bot message on the left */
        }

        /* Sticky question input bar */
        .input-container {
            position: fixed;
            bottom: 20px;
            left: 20px;
            right: 20px;
            padding: 10px;
            background-color: #fff;
            z-index: 10;
            display: flex;
            align-items: center;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }

        .input-container input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 20px;
        }

        .input-container button {
            margin-left: 10px;
            padding: 10px 15px;
            border-radius: 20px;
            background-color: #128C7E;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Chat Interface
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display the chat history with correct alignment
for sender, message in st.session_state.chat_history:
    message_style = "user-message" if sender == "You" else "bot-message"
    st.markdown(f"""
        <div class='message {message_style}'>{message}</div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input Box with Send Button (Fixed at the Bottom)
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
question = st.text_input("Type a message...", key="question_input", placeholder="Ask something...", label_visibility="collapsed")
if st.button("Send", key="send_button"):
    st.session_state.chat_history.append(("You", question))
    st.session_state["processing"] = True  # Show processing message
    st.rerun()  # Refresh UI immediately

st.markdown("</div>", unsafe_allow_html=True)

# Replace the localhost URL with your Render backend URL
BACKEND_URL = "https://bot-me-backend.onrender.com"
# BACKEND_URL = "http://localhost:8000"

# Processing Message
if "processing" in st.session_state and st.session_state["processing"]:
    with st.spinner("🤖 BOT-ME is thinking..."):
        time.sleep(2)  # Simulate processing delay

        # Fetch response from backend
        response = requests.post(f"{BACKEND_URL}/ask", json={"question": question})
        if response.status_code == 200:
            answer = response.json().get("response", "Sorry, I couldn't understand that.")

            # Append bot response and remove processing state
            st.session_state.chat_history.append(("Bot", answer))
            st.session_state["processing"] = False

            # Speak the response
            speak(answer)
        else:
            st.error("Error connecting to the backend. Please try again later.")

        # Refresh UI to show response
        st.rerun()
