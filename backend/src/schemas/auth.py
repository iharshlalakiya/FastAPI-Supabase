from pydantic import BaseModel, EmailStr, Field

class SignUpSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str = Field(min_length=6)
    confirm_password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str