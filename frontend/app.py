import streamlit as st
import requests
import pyttsx3

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Title and Description
st.title("BOT-ME: AI Assistant")
st.write("This chatbot can answer questions based on predefined data from a PDF.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat Interface
question = st.text_input("Ask me anything:")
if st.button("Send"):
    if question:
        response = requests.post("http://localhost:8000/ask", json={"question": question})
        if response.status_code == 200:
            answer = response.json().get("response", "Sorry, I couldn't understand that.")

            # Save to chat history
            st.session_state.chat_history.append(("You", question))
            st.session_state.chat_history.append(("BOT-ME", answer))

            # Speak the response
            engine.say(answer)
            engine.runAndWait()

        else:
            st.error("Error connecting to the backend. Please try again later.")

# Display chat history
for sender, message in st.session_state.chat_history:
    st.write(f"**{sender}:** {message}")
