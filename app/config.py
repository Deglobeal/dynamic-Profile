from pydsntic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "Profile API"
    debug: bool = False
    cat_fact_timeout: int = 8
    cat_fact_url: str = "https://catfact.ninja/fact"
    database_url: Optional[str] = None


# my personal informantion  

    user_email: str = "kachimaxy2@gmail.com"
    user_name: str = " Gerard Ugwu Onyedikachi"
    user_stack: str = "Python, FastAPI, Django, Flask, SQLAlchemy, PostgreSQL, Docker, Kubernetes"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()