# Import Pydantic models and types for data validation
from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    """
    Schema representing the payload for a user registration request.
    """
    # First name with validation: minimum 2 characters, whitespace stripped
    name: str = Field(..., min_length=2, strip_whitespace=True)
    # Last name with validation: minimum 2 characters, whitespace stripped
    surname: str = Field(..., min_length=2, strip_whitespace=True)
    # Email address validated for correct format
    email: EmailStr
    # Password with validation: min 8 chars, max 100 chars, whitespace stripped
    password: str = Field(..., min_length=8, max_length=100, strip_whitespace=True)

class LoginRequest(BaseModel):
    """
    Schema representing the payload for a user login request.
    """
    email: EmailStr
    # Password is required (minimum 1 character)
    password: str = Field(..., min_length=1, strip_whitespace=True)

class RegisterResponse(BaseModel):
    """
    Schema for the response returned after a successful registration.
    """
    message: str
    doctor_id: int

class LoginResponse(BaseModel):
    """
    Schema for the response returned after a successful login.
    Contains the JWT token for authentication.
    """
    message: str
    jwt_token: str