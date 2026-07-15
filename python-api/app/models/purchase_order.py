import enum
from sqlalchemy import Column, Integer, String, Date, Numeric, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class PurchaseOrderStatus(str, enum.Enum):
    brouillon = "brouillon"
    envoyee = "envoyée"
    recue = "reçue"
    annulee = "annulée"


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    order_date = Column(Date, server_default=func.now())
    expected_date = Column(Date, nullable=True)
    status = Column(Enum(PurchaseOrderStatus), default=PurchaseOrderStatus.brouillon)
    total_amount = Column(Numeric(10, 2), default=0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    supplier = relationship("Supplier", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")


class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"

    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    purchase_order = relationship("PurchaseOrder", back_populates="items")
    product = relationship("Product")
