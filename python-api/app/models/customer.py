import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class CustomerType(str, enum.Enum):
    particulier = "particulier"
    entreprise = "entreprise"


class CustomerStatus(str, enum.Enum):
    actif = "actif"
    inactif = "inactif"


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(CustomerType), default=CustomerType.entreprise)
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(String(255))
    status = Column(Enum(CustomerStatus), default=CustomerStatus.actif)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    sales_orders = relationship("SalesOrder", back_populates="customer")
