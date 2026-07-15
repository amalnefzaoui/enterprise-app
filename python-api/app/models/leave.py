import enum
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class LeaveType(str, enum.Enum):
    conge_paye = "congé_payé"
    maladie = "maladie"
    sans_solde = "sans_solde"
    autre = "autre"


class LeaveStatus(str, enum.Enum):
    en_attente = "en_attente"
    approuve = "approuvé"
    refuse = "refusé"


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    type = Column(Enum(LeaveType), default=LeaveType.conge_paye)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days_count = Column(Integer, nullable=False)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.en_attente)
    reason = Column(Text)
    approved_by = Column(Integer, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    employee = relationship("Employee", back_populates="leaves")
