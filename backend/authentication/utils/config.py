from pydantic import BaseSettings

class AuthSettings(BaseSettings):
    jwt_secret: str
    jwt_expires_minutes: int

    class Config:
        env_file = ".env"

settings = AuthSettings()