from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.models.leave import LeaveType, LeaveStatus


class LeaveCreate(BaseModel):
    employee_id: int
    type: LeaveType = LeaveType.conge_paye
    start_date: date
    end_date: date
    reason: Optional[str] = None


class LeaveStatusUpdate(BaseModel):
    status: LeaveStatus
    approved_by: Optional[int] = None


class LeaveOut(BaseModel):
    id: int
    employee_id: int
    type: LeaveType
    start_date: date
    end_date: date
    days_count: int
    status: LeaveStatus
    reason: Optional[str]

    class Config:
        from_attributes = True
