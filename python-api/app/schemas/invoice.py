from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import BaseModel

from app.models.invoice import InvoiceType, InvoiceStatus


class InvoiceCreate(BaseModel):
    type: InvoiceType
    reference_order_id: int
    due_date: Optional[date] = None


class InvoiceStatusUpdate(BaseModel):
    status: InvoiceStatus


class InvoiceOut(BaseModel):
    id: int
    invoice_number: str
    type: InvoiceType
    reference_order_id: int
    amount: Decimal
    issue_date: Optional[date]
    due_date: Optional[date]
    status: InvoiceStatus

    class Config:
        from_attributes = True
