import enum
from sqlalchemy import Column, Integer, String, Date, Enum, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class EmployeeStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    position = Column(String(150))
    department = Column(String(150))
    hire_date = Column(Date)
    leave_balance = Column(Integer, default=25)
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.active)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="employee", uselist=False)
    leaves = relationship("Leave", back_populates="employee")
    attendances = relationship("Attendance", back_populates="employee")
