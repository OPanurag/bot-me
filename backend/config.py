import os

# Load API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Ensure API keys are set
if not OPENAI_API_KEY or not GEMINI_API_KEY:
    print("⚠️ Warning: API keys are missing. Set them as environment variables.")