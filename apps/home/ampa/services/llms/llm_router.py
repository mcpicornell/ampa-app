from functools import lru_cache

from django.conf import settings
from litellm import Router

GEMINI_2_5_FLASH = settings.GEMINI_2_5_FLASH
GEMINI_2_5_FLASH_LITE = settings.GEMINI_2_5_FLASH_LITE
GEMINI_3_5_FLASH = settings.GEMINI_3_5_FLASH
GEMINI_3_1_FLASH_LITE = settings.GEMINI_3_1_FLASH_LITE
GEMINI_API_KEY = settings.GEMINI_API_KEY

MODEL_LIST = [
    {
        "model_name": GEMINI_3_1_FLASH_LITE,
        "litellm_params": {"model": GEMINI_3_1_FLASH_LITE, "api_key": GEMINI_API_KEY},
    },
    {
        "model_name": GEMINI_2_5_FLASH_LITE,
        "litellm_params": {"model": GEMINI_2_5_FLASH_LITE, "api_key": GEMINI_API_KEY},
    },
    {
        "model_name": GEMINI_3_5_FLASH,
        "litellm_params": {"model": GEMINI_3_5_FLASH, "api_key": GEMINI_API_KEY},
    },
    {
        "model_name": GEMINI_2_5_FLASH,
        "litellm_params": {"model": GEMINI_2_5_FLASH},
    },
]
FALLBACKS = [
    {
        GEMINI_3_1_FLASH_LITE: [
            GEMINI_2_5_FLASH_LITE,
            GEMINI_3_5_FLASH,
            GEMINI_2_5_FLASH,
        ]
    },
    {
        GEMINI_2_5_FLASH_LITE: [
            GEMINI_3_5_FLASH,
            GEMINI_2_5_FLASH,
        ]
    },
    {
        GEMINI_3_5_FLASH: [
            GEMINI_2_5_FLASH,
        ]
    },
]
NUM_RETRIES = 0


@lru_cache
def get_llm_router() -> Router:
    return Router(
        model_list=MODEL_LIST,
        fallbacks=FALLBACKS,
        num_retries=NUM_RETRIES,
    )
