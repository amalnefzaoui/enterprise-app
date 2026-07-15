from typing import Optional, List
from datetime import date
from decimal import Decimal
from pydantic import BaseModel

from app.models.purchase_order import PurchaseOrderStatus
from app.models.sales_order import SalesOrderStatus


# ---- Purchase Order ----
class PurchaseOrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_cost: Decimal


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    expected_date: Optional[date] = None
    items: List[PurchaseOrderItemCreate]


class OrderStatusUpdate(BaseModel):
    status: str


class PurchaseOrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_cost: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class PurchaseOrderOut(BaseModel):
    id: int
    supplier_id: int
    order_date: Optional[date]
    expected_date: Optional[date]
    status: PurchaseOrderStatus
    total_amount: Decimal
    items: List[PurchaseOrderItemOut] = []

    class Config:
        from_attributes = True


# ---- Sales Order ----
class SalesOrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal


class SalesOrderCreate(BaseModel):
    customer_id: int
    items: List[SalesOrderItemCreate]


class SalesOrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class SalesOrderOut(BaseModel):
    id: int
    customer_id: int
    order_date: Optional[date]
    status: SalesOrderStatus
    total_amount: Decimal
    items: List[SalesOrderItemOut] = []

    class Config:
        from_attributes = True
