import random
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.invoice import Invoice, InvoiceType
from app.models.purchase_order import PurchaseOrder
from app.models.sales_order import SalesOrder
from app.schemas.invoice import InvoiceCreate, InvoiceStatusUpdate, InvoiceOut
from app.auth.dependencies import require_role

router = APIRouter(prefix="/api/invoices", tags=["invoices"])


def generate_invoice_number(invoice_type: InvoiceType) -> str:
    prefix = "FA" if invoice_type == InvoiceType.achat else "FV"
    year = datetime.now().year
    suffix = random.randint(100000, 999999)
    return f"{prefix}-{year}-{suffix}"


@router.get("/", response_model=list[InvoiceOut])
def list_invoices(
    type_filter: str | None = None,
    status_filter: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Invoice)
    if type_filter:
        query = query.filter(Invoice.type == type_filter)
    if status_filter:
        query = query.filter(Invoice.status == status_filter)
    return query.order_by(Invoice.issue_date.desc()).all()


@router.post("/", response_model=InvoiceOut, status_code=status.HTTP_201_CREATED)
def create_invoice(
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
    _user=Depends(require_role("admin", "manager")),
):
    if payload.type == InvoiceType.achat:
        order = db.query(PurchaseOrder).filter(PurchaseOrder.id == payload.reference_order_id).first()
    else:
        order = db.query(SalesOrder).filter(SalesOrder.id == payload.reference_order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Commande de référence non trouvée")

    invoice = Invoice(
        invoice_number=generate_invoice_number(payload.type),
        type=payload.type,
        reference_order_id=payload.reference_order_id,
        amount=order.total_amount,
        due_date=payload.due_date,
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@router.patch("/{invoice_id}/status", response_model=InvoiceOut)
def update_invoice_status(
    invoice_id: int,
    payload: InvoiceStatusUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_role("admin", "manager")),
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Facture non trouvée")

    invoice.status = payload.status
    db.commit()
    db.refresh(invoice)
    return invoice
