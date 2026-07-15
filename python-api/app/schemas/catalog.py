from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, EmailStr

from app.models.supplier import SupplierStatus
from app.models.customer import CustomerType, CustomerStatus


# ---- Supplier ----
class SupplierCreate(BaseModel):
    name: str
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class SupplierOut(BaseModel):
    id: int
    name: str
    contact_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    status: SupplierStatus

    class Config:
        from_attributes = True


# ---- Customer ----
class CustomerCreate(BaseModel):
    name: str
    type: CustomerType = CustomerType.entreprise
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class CustomerOut(BaseModel):
    id: int
    name: str
    type: CustomerType
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    status: CustomerStatus

    class Config:
        from_attributes = True


# ---- Product ----
class ProductCreate(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    unit_cost: Decimal = 0
    unit_price: Decimal = 0
    stock_quantity: int = 0
    reorder_level: int = 10
    supplier_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    unit_cost: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None
    reorder_level: Optional[int] = None
    supplier_id: Optional[int] = None


class StockAdjustment(BaseModel):
    quantity: int
    operation: str  # "add" | "remove" | "set"


class ProductOut(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str]
    category: Optional[str]
    unit_cost: Decimal
    unit_price: Decimal
    stock_quantity: int
    reorder_level: int
    supplier_id: Optional[int]
    low_stock: bool

    class Config:
        from_attributes = True
