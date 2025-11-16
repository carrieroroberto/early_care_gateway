from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: int
    email: EmailStr
    password_hash: str
    reset_token_hash: Optional[str] = None