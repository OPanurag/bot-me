import openai
import json
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_embeddings(text):
    """Convert text into OpenAI embeddings."""
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

def save_embeddings(text, file_path="knowledge.json"):
    """Store embeddings for future retrieval."""
    embeddings = generate_embeddings(text)
    with open(file_path, "w") as f:
        json.dump({"text": text, "embedding": embeddings}, f)

def load_knowledge(file_path="knowledge.json"):
    """Load stored knowledge from a file."""
    with open(file_path, "r") as f:
        return json.load(f)["text"]
