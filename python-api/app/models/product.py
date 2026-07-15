from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(150))
    unit_cost = Column(Numeric(10, 2), default=0)   # prix d'achat
    unit_price = Column(Numeric(10, 2), default=0)  # prix de vente
    stock_quantity = Column(Integer, default=0)
    reorder_level = Column(Integer, default=10)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    supplier = relationship("Supplier", back_populates="products")

    @property
    def low_stock(self) -> bool:
        return self.stock_quantity <= self.reorder_level
