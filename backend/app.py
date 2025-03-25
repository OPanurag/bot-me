from fastapi import FastAPI, UploadFile, File
import json
from openai import OpenAI
from process_pdf import extract_text_from_pdf
from config import OPENAI_API_KEY
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=OPENAI_API_KEY)

# Load user data
with open("user_data.json", "r", encoding="utf-8") as f:
    user_data = json.load(f)

def generate_response(question):
    """Generate response using ChatGPT API."""
    prompt = f"Based on this data: {user_data}, answer this: {question}"
    response = client.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@app.post("/ask")
async def ask(data: dict):
    question = data.get("question", "")
    answer = generate_response(question)
    return {"response": answer}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)
    with open("user_data.json", "w", encoding="utf-8") as f:
        json.dump({"data": text}, f)
    return {"message": "PDF data saved successfully"}
