import os

# Load API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD7kixKh3f6ttdBg54Tr7kJhEatv8ECDgA")

# Ensure API keys are set
if not OPENAI_API_KEY or not GEMINI_API_KEY:
    print("⚠️ Warning: API keys are missing. Set them as environment variables.")