from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    message: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str    