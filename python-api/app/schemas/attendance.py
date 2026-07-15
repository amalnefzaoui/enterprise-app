from datetime import date, time
from pydantic import BaseModel

from app.models.attendance import AttendanceStatus


class AttendanceAction(BaseModel):
    employee_id: int


class AttendanceOut(BaseModel):
    id: int
    employee_id: int
    date: date
    check_in: time | None
    check_out: time | None
    status: AttendanceStatus

    class Config:
        from_attributes = True
