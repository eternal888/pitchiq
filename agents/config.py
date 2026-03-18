from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Load .env once here — not in every file
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# One LLM instance for smart tasks
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY
)

# Cheaper LLM for simple tasks like critic
llm_lite = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=GEMINI_API_KEY
)