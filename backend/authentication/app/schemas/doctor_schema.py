# Import Pydantic components for data modeling and validation
from pydantic import BaseModel, EmailStr, Field

class RegisterDoctorRequest(BaseModel):
    """
    Schema for the doctor registration request payload.
    Validates input fields before processing.
    """
    # Doctor's first name: required, min 2 chars, whitespace stripped
    name: str = Field(..., min_length=2, strip_whitespace=True)
    # Doctor's last name: required, min 2 chars, whitespace stripped
    surname: str = Field(..., min_length=2, strip_whitespace=True)
    # Validates that the input is a valid email address format
    email: EmailStr
    # Password: required, min 8 chars, max 100 chars, whitespace stripped
    password: str = Field(..., min_length=8, max_length=100, strip_whitespace=True)

class LoginDoctorRequest(BaseModel):
    """
    Schema for the doctor login request payload.
    """
    email: EmailStr
    # Password is required (at least 1 char)
    password: str = Field(..., min_length=1, strip_whitespace=True)

class ValidateTokenRequest(BaseModel):
    """
    Schema for the token validation request.
    Used when other services need to verify a token.
    """
    # The JWT token string to be validated
    token: str = Field(..., min_length=1, strip_whitespace=True)

class RegisterDoctorResponse(BaseModel):
    """
    Schema for the response after a successful registration.
    """
    # Default success message
    message: str = "Doctor registered successfully"
    # The ID of the newly created doctor
    doctor_id: int

class LoginDoctorResponse(BaseModel):
    """
    Schema for the response after a successful login.
    """
    # Default success message
    message: str = "Doctor logged in successfully"
    # The generated JWT token
    jwt_token: str

class ValidateTokenResponse(BaseModel):
    """
    Schema for the response after validating a token.
    """
    # Default success message
    message: str = "JWT Token validated successfully"
    # The ID of the doctor associated with the valid token
    doctor_id: int