import enum
from sqlalchemy import Column, Integer, String, Date, Numeric, Enum, DateTime, func

from app.database import Base


class InvoiceType(str, enum.Enum):
    achat = "achat"
    vente = "vente"


class InvoiceStatus(str, enum.Enum):
    payee = "payée"
    impayee = "impayée"
    en_retard = "en_retard"


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    type = Column(Enum(InvoiceType), nullable=False)
    reference_order_id = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    issue_date = Column(Date, server_default=func.now())
    due_date = Column(Date, nullable=True)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.impayee)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
