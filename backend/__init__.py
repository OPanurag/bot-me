"""
Backend package initialization.

This file initializes the backend package and makes its modules available for import.
"""

# Import necessary modules to make them available when importing the backend package
from fastapi import FastAPI
import json
import requests
from backend.pdf_to_json import extract_text_from_pdf
from backend.config import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import openai

# Version information
__version__ = "0.1.0"