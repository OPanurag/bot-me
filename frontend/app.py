import streamlit as st
import requests
import time
import pyttsx3
import threading

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to speak text in a separate thread
def speak(text):
    def run():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

# Title and Description
st.title("🤖 BOT-ME: AI Assistant")
st.write("This chatbot can answer questions based on predefined data from a PDF.")

# Chat Interface
question = st.text_input("Ask me anything:")

if st.button("Send"):
    if question:
        # Step 1: Append user's question
        st.session_state.chat_history.append(("You", question))
        st.session_state["processing"] = True  # Show processing message
        st.rerun()  # Refresh UI immediately

# Show chat history first
st.write("---")
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"""
        <div style="text-align: right; background-color: #ADD8E6; color: black; padding: 10px; 
                    border-radius: 10px; margin: 5px 0 5px 30%; animation: fadeIn 0.5s;">
            {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align: left; background-color: #E3E3E3; color: black; padding: 10px; 
                    border-radius: 10px; margin: 5px 30% 5px 0; animation: fadeIn 0.5s;">
            {message}
        </div>
        """, unsafe_allow_html=True)

# Processing Message
if "processing" in st.session_state and st.session_state["processing"]:
    with st.spinner("🤖 BOT-ME is thinking..."):
        time.sleep(2)  # Simulate processing delay

        # Fetch response from backend
        response = requests.post("http://localhost:8000/ask", json={"question": question})
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
        st.experimental_rerun()

# Add CSS for animations
st.markdown("""
    <style>
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)
