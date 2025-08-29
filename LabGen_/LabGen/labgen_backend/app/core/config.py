import os

# In a real application, this would be handled by a more robust solution like
# Pydantic's BaseSettings to load from .env files and perform validation.
# For this skeleton, we read directly from environment variables.

# Determines the media generation backend.
# Supported values: "openai", "huggingface"
GENERATION_BACKEND = os.getenv("GENERATION_BACKEND", "huggingface").lower()

# Example of other settings you might have:
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("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")
# DATABASE_URL = os.getenv("DATABASE_URL")
# S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
