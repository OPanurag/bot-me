import streamlit as st
import requests

# Title and Description
st.title("BOT-ME: AI Assistant")
st.write("This chatbot can answer questions based on predefined data from a PDF.")

# Chat Interface
question = st.text_input("Ask me anything:")
if st.button("Send"):
    if question:
        response = requests.post("http://localhost:8000/ask", json={"question": question})
        if response.status_code == 200:
            answer = response.json().get("response", "Sorry, I couldn't understand that.")
            st.write(f"**BOT-ME:** {answer}")
        else:
            st.error("Error connecting to the backend. Please try again later.")
