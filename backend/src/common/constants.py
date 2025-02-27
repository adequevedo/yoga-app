import os
from utils.config import ConfigHelper

ALL_MODEL_SETTINGS = ConfigHelper("configs/settings.json").get_config("all", "llm")
ALL_CONFIGS = ConfigHelper("configs/settings.json")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SEARCH_ENGINE_URL = os.getenv("SEARCH_ENGINE_URL")
SEARCH_ENGINE_API_KEY = os.getenv("SEARCH_ENGINE_API_KEY")
SEARCH_ENGINE_CX = os.getenv("SEARCH_ENGINE_CX")