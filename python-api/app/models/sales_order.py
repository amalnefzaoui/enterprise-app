import enum
from sqlalchemy import Column, Integer, String, Date, Numeric, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class SalesOrderStatus(str, enum.Enum):
    brouillon = "brouillon"
    confirmee = "confirmée"
    livree = "livrée"
    annulee = "annulée"


class SalesOrder(Base):
    __tablename__ = "sales_orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_date = Column(Date, server_default=func.now())
    status = Column(Enum(SalesOrderStatus), default=SalesOrderStatus.brouillon)
    total_amount = Column(Numeric(10, 2), default=0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="sales_orders")
    items = relationship("SalesOrderItem", back_populates="sales_order", cascade="all, delete-orphan")


class SalesOrderItem(Base):
    __tablename__ = "sales_order_items"

    id = Column(Integer, primary_key=True, index=True)
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    sales_order = relationship("SalesOrder", back_populates="items")
    product = relationship("Product")
