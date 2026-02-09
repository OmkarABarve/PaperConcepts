import os
from typing import Final
import google.generativeai as genai
from dotenv import load_dotenv

MODEL_FAST: Final[str] = "gemini-2.5-flash"
MODEL_STRICT: Final[str] = "gemini-2.5-flash"

def configure_gemini() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set in .env")
    genai.configure(api_key=api_key)