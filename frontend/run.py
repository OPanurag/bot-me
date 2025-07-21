# frontend/run.py

import gradio as gr
import requests

# Backend endpoint
BACKEND_URL = "http://localhost:8000/ask"

def chatbot_fn(message, history):
    try:
        response = requests.post(BACKEND_URL, json={"question": message})
        if response.status_code == 200:
            reply = response.json().get("response", "Sorry, I couldn't understand that.")
        else:
            reply = "⚠️ Error from backend."
    except Exception as e:
        reply = f"⚠️ Exception: {e}"
    history.append((message, reply))
    return "", history

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🤖 BOT-ME: Ask your PDF-based AI Assistant")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask something...", label="Your Message")
    clear = gr.Button("Clear Chat")

    msg.submit(chatbot_fn, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(server_name="0.0.0.0", server_port=8501)
