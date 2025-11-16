from pydantic import BaseSettings

class AuthSettings(BaseSettings):
    db_url: str

    class Config:
        env_file = ".env"

settings = AuthSettings()