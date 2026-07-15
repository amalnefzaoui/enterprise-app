import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class SupplierStatus(str, enum.Enum):
    actif = "actif"
    inactif = "inactif"


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_name = Column(String(150))
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(String(255))
    status = Column(Enum(SupplierStatus), default=SupplierStatus.actif)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    products = relationship("Product", back_populates="supplier")
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")
