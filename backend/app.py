from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
from process_pdf import extract_text_from_pdf
from vector_store import save_embeddings, load_knowledge
from config import OPENAI_API_KEY

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = OPENAI_API_KEY

# Extract text from PDF and store knowledge
pdf_text = extract_text_from_pdf("user_data.pdf")
save_embeddings(pdf_text)

def generate_response(question):
    """Generate AI response based on stored knowledge."""
    knowledge = load_knowledge()
    prompt = f"Based on this information: {knowledge}, answer this: {question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

@app.post("/ask")
async def ask(request: Request):
    """Receive questions and return AI-generated responses."""
    data = await request.json()
    question = data.get("question", "")
    answer = generate_response(question)
    return {"response": answer}
