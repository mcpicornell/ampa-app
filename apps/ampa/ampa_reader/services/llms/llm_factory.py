from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI


@lru_cache
def get_google_llm(model: str, api_key: str, temperature: int = 0):
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=temperature,
    )
