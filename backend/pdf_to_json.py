import fitz  # PyMuPDF
import json
import os

PDF_PATH = "data/profile.pdf"
JSON_PATH = "user_data.json"

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text.strip()

def save_text_as_json(text, json_path):
    data = {"user_profile": text}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    text = extract_text_from_pdf(PDF_PATH)
    save_text_as_json(text, JSON_PATH)
    print(f"User profile extracted and saved to {JSON_PATH}")
