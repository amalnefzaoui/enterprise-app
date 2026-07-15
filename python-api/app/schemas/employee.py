from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr

from app.models.employee import EmployeeStatus


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    position: Optional[str] = None
    department: Optional[str] = None
    hire_date: Optional[date] = None


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    position: Optional[str] = None
    department: Optional[str] = None
    status: Optional[EmployeeStatus] = None
    leave_balance: Optional[int] = None


class EmployeeOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    position: Optional[str]
    department: Optional[str]
    hire_date: Optional[date]
    leave_balance: int
    status: EmployeeStatus

    class Config:
        from_attributes = True
