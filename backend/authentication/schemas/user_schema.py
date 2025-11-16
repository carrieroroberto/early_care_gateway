from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str

class UserReadDTO(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class UserUpdateDTO(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None