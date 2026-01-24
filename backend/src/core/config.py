from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    database_url: str = "sqlite:///./todo_app.db"  # Using SQLite for local development

    # JWT settings
    jwt_secret_key: str 
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Better Auth settings
    better_auth_secret: str
    
     # API config
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    log_level: str = "info"

    class Config:
        env_file = ".env"
        


# Create a singleton instance of settings
settings = Settings()