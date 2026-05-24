from functools import lru_cache

from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI


@lru_cache
def get_google_llm(model: str | None = None, temperature: int = 0):
    return ChatGoogleGenerativeAI(
        model=model or settings.GOOGLE_LLM_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=temperature,
    )
