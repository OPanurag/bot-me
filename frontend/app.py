import streamlit as st
import requests

st.title("BOT-ME: Chat with Your AI")

st.write("Upload a PDF to train the bot on your data.")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
if uploaded_file:
    response = requests.post("http://localhost:8000/upload-pdf", files={"file": uploaded_file.getvalue()})
    st.success("PDF uploaded and processed!")

# Chat Interface
question = st.text_input("Ask me anything:")
if st.button("Send"):
    if question:
        response = requests.post("http://localhost:8000/ask", json={"question": question})
        answer = response.json()["response"]
        st.write(f"**BOT-ME:** {answer}")
