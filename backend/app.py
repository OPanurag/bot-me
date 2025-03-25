from fastapi import FastAPI
import json
from openai import OpenAI
from pdf_to_json import extract_text_from_pdf
from config import OPENAI_API_KEY
from fastapi.middleware.cors import CORSMiddleware

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
client = OpenAI(api_key=OPENAI_API_KEY)

# Extract and save PDF data (No user upload required)
PDF_PATH = "backend/data/profile.pdf"
JSON_PATH = "backend/user_data.json"

text_data = extract_text_from_pdf(PDF_PATH)
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump({"data": text_data}, f)

# Load the saved JSON data
with open(JSON_PATH, "r", encoding="utf-8") as f:
    user_data = json.load(f)

def generate_response(question):
    """Generate response using OpenAI ChatGPT API."""
    prompt = f"Based on this data: {user_data['data']}, answer this: {question}"
    response = client.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

@app.get("/")
def read_root():
    return {"message": "Chatbot API is running!"}

@app.post("/ask")
async def ask(data: dict):
    question = data.get("question", "")
    answer = generate_response(question)
    return {"response": answer}
