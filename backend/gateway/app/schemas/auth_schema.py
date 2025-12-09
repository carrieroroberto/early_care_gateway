from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, strip_whitespace=True)
    surname: str = Field(..., min_length=2, strip_whitespace=True)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100, strip_whitespace=True)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, strip_whitespace=True)

class RegisterResponse(BaseModel):
    message: str
    doctor_id: int

class LoginResponse(BaseModel):
    message: str
    jwt_token: str