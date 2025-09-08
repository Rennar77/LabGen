import os
from dotenv import load_dotenv

load_dotenv() 

# Determines the media generation backend.
GENERATION_BACKEND = os.getenv("GENERATION_BACKEND", "huggingface").lower()

# API keys (loaded from .env instead of hardcoding)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
# DATABASE_URL = os.getenv("DATABASE_URL")
# S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
