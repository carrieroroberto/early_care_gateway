from pydantic import BaseModel, EmailStr, Field

class RegisterDoctorRequest(BaseModel):
    name: str = Field(..., min_length=2, strip_whitespace=True)
    surname: str = Field(..., min_length=2, strip_whitespace=True)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100, strip_whitespace=True)

class LoginDoctorRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, strip_whitespace=True)

class ValidateTokenRequest(BaseModel):
    token: str = Field(..., min_length=1, strip_whitespace=True)

class RegisterDoctorResponse(BaseModel):
    message: str = "Doctor registered successfully"
    doctor_id: int

class LoginDoctorResponse(BaseModel):
    message: str = "Doctor logged in successfully"
    jwt_token: str

class ValidateTokenResponse(BaseModel):
    message: str = "JWT Token validated successfully"
    doctor_id: int