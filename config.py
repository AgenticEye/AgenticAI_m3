from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str

settings = Settings()