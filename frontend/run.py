import streamlit as st
import requests
import time

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title and Description
st.title("🤖 BOT-ME: AI Assistant")
st.write("This chatbot can answer questions based on predefined data from a PDF.")

# Custom CSS to style the chat interface
st.markdown("""
    <style>
        body {
            margin: 0;
            padding: 0;
        }

        .css-1v3fvcr, .css-18e3th9 {
            background: transparent !important;
            padding: 0 !important;
        }

        .chat-container {
            max-height: 50vh;
            overflow-y: auto;
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

        .message {
            max-width: 70%;
            word-wrap: break-word;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            font-size: 16px;
            display: inline-block;
            color: black;
        }

        .user-message {
            background-color: #DCF8C6;
            text-align: right;
            align-self: flex-end;
        }

        .bot-message {
            background-color: #E3E3E3;
            text-align: left;
            align-self: flex-start;
        }

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

# Chat Display
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for sender, message in st.session_state.chat_history:
    message_style = "user-message" if sender == "You" else "bot-message"
    st.markdown(f"""
        <div class='message {message_style}'>{message}</div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Input field fixed at the bottom
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
question = st.text_input("Type a message...", key="question_input", placeholder="Ask something...", label_visibility="collapsed")
if st.button("Send", key="send_button"):
    st.session_state.chat_history.append(("You", question))
    st.session_state["processing"] = True
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Backend URL
# BACKEND_URL = "https://bot-me-backend.onrender.com"
BACKEND_URL = "http://localhost:8000"

# Processing and response handling
if "processing" in st.session_state and st.session_state["processing"]:
    with st.spinner("🤖 BOT-ME is thinking..."):
        time.sleep(1.5)  # Optional delay to simulate thinking
        try:
            response = requests.post(f"{BACKEND_URL}/ask", json={"question": question})
            if response.status_code == 200:
                answer = response.json().get("response", "Sorry, I couldn't understand that.")
                st.session_state.chat_history.append(("Bot", answer))
            else:
                st.session_state.chat_history.append(("Bot", "Error connecting to backend."))
        except Exception as e:
            st.session_state.chat_history.append(("Bot", f"Request failed: {e}"))

        st.session_state["processing"] = False
        st.rerun()
