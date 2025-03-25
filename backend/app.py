from fastapi import FastAPI
import json
from backend.pdf_to_json import extract_text_from_pdf
from backend.config import OPENAI_API_KEY
from fastapi.middleware.cors import CORSMiddleware

import openai
import time
from openai import OpenAI
from openai._exceptions import RateLimitError, APIConnectionError

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


# Function to generate AI response
def generate_response(question: str):
    time.sleep(2)  # Small delay to prevent excessive API calls
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content.strip()
    except RateLimitError:
        return "API quota exceeded. Please check your OpenAI plan."
    except APIConnectionError:
        return "Error connecting to OpenAI. Please check your internet connection."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


@app.get("/")
def read_root():
    return {"message": "Chatbot API is running!"}


@app.post("/ask")
async def ask(data: dict):
    question = data.get("question", "")
    answer = generate_response(question)
    return {"response": answer}  # Return only text response
