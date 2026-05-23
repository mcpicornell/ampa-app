from functools import lru_cache

from decouple import config
from langchain_google_genai import ChatGoogleGenerativeAI


@lru_cache
def get_llm(model: str | None = None):
    return ChatGoogleGenerativeAI(
        model=model or config("LLM_MODEL", default="gemini-2.5-flash"),
        google_api_key=config("GOOGLE_API_KEY"),
    )
