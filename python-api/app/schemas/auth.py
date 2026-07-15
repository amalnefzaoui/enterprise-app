from typing import Optional
from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.employee
    employee_id: Optional[int] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    token: str
    user: UserOut


class CurrentUser(BaseModel):
    id: int
    email: str
    role: str
    employee_id: Optional[int] = None
