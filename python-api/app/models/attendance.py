import enum
from sqlalchemy import Column, Integer, String, Date, Time, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class AttendanceStatus(str, enum.Enum):
    present = "présent"
    absent = "absent"
    retard = "retard"
    conge = "congé"


class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)
    check_in = Column(Time, nullable=True)
    check_out = Column(Time, nullable=True)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.present)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    employee = relationship("Employee", back_populates="attendances")
