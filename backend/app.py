from fastapi import FastAPI
import json
import requests
from backend.pdf_to_json import extract_text_from_pdf
from backend.config import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import openai

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI API Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Extract and save PDF data (No user upload required)
PDF_PATH = "backend/data/profile.pdf"
JSON_PATH = "backend/user_data.json"

text_data = extract_text_from_pdf(PDF_PATH)
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump({"data": text_data}, f)

# Load the saved JSON data
with open(JSON_PATH, "r", encoding="utf-8") as f:
    user_data = json.load(f).get("data", "")

# Store conversation history in memory
conversation_history = []


# ✅ **Function to generate response using OpenAI (GPT)**
def generate_chatgpt_response(question: str, context: str):
    prompt = f"""You are an AI assistant. Answer the user's question based strictly on the provided knowledge base.

    Knowledge Base:
    {context}

    User: {question}
    AI:"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Switch to "gpt-4" if needed
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"


# ✅ **Function to generate response using Gemini API**
def generate_gemini_response(question: str, context: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "contents": [
            {"role": "user", "parts": [{"text": f"Use the following knowledge base to answer the question:\n\n{context}\n\nUser: {question}"}]}
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError):
            return "Error parsing response from Gemini API."
    else:
        return f"Error: {response.status_code}, {response.json()}"


@app.get("/")
def read_root():
    return {"message": "Chatbot API is running!"}


# ✅ **Unified `/ask` Endpoint**
@app.post("/ask")
async def ask(data: dict):
    global conversation_history  # Track conversation history

    question = data.get("question", "").strip()

    # **Step 1: Reset conversation if a new question is asked mid-way**
    if len(conversation_history) > 5:  # Limit history to recent 5 messages
        conversation_history.pop(0)

    # **Step 2: Store latest question in history**
    conversation_history.append({"user": question})

    # **Step 3: Generate responses from models**
    # response = generate_chatgpt_response(question, user_data)  # OpenAI GPT Response
    response = generate_gemini_response(question, user_data)   # Google Gemini Response

    # **Step 4: Store response in history and return**
    conversation_history.append({"bot": response})
    return JSONResponse(content={"response": response, "history": conversation_history})
