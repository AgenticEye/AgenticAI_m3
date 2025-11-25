# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AIMLAPI_API_KEY = os.getenv("AIMLAPI_API_KEY", "")
    PYTRENDS_TIMEFRAME = os.getenv("PYTRENDS_TIMEFRAME", "now 7-d")

CONFIG = Config()