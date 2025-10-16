from pydantic import BaseModel, EmailStr

class RegisterIn(BaseModel):
    email: EmailStr
    name: str
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    accessToken: str
    refreshToken: str | None = None