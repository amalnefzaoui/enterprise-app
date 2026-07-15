from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.purchase_order import PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatus
from app.models.product import Product
from app.schemas.orders import PurchaseOrderCreate, PurchaseOrderOut, OrderStatusUpdate
from app.auth.dependencies import require_role

router = APIRouter(prefix="/api/purchase-orders", tags=["purchase-orders"])


@router.get("/", response_model=list[PurchaseOrderOut])
def list_purchase_orders(
    status_filter: str | None = None,
    supplier_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(PurchaseOrder).options(joinedload(PurchaseOrder.items))
    if status_filter:
        query = query.filter(PurchaseOrder.status == status_filter)
    if supplier_id:
        query = query.filter(PurchaseOrder.supplier_id == supplier_id)
    return query.order_by(PurchaseOrder.created_at.desc()).all()


@router.get("/{order_id}", response_model=PurchaseOrderOut)
def get_purchase_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(PurchaseOrder).options(joinedload(PurchaseOrder.items)).filter(
        PurchaseOrder.id == order_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order


@router.post("/", response_model=PurchaseOrderOut, status_code=status.HTTP_201_CREATED)
def create_purchase_order(payload: PurchaseOrderCreate, db: Session = Depends(get_db)):
    if not payload.items:
        raise HTTPException(status_code=400, detail="La commande doit contenir au moins un produit")

    total_amount = sum(item.quantity * item.unit_cost for item in payload.items)

    order = PurchaseOrder(
        supplier_id=payload.supplier_id,
        expected_date=payload.expected_date,
        total_amount=total_amount,
        status=PurchaseOrderStatus.brouillon,
    )
    db.add(order)
    db.flush()  # récupère order.id sans commit

    for item in payload.items:
        db.add(PurchaseOrderItem(
            purchase_order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_cost=item.unit_cost,
            subtotal=item.quantity * item.unit_cost,
        ))

    db.commit()
    db.refresh(order)
    return order


@router.patch("/{order_id}/status", response_model=PurchaseOrderOut)
def update_purchase_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_role("admin", "manager")),
):
    order = db.query(PurchaseOrder).options(joinedload(PurchaseOrder.items)).filter(
        PurchaseOrder.id == order_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    was_already_received = order.status == PurchaseOrderStatus.recue
    order.status = payload.status

    # Incrémente le stock une seule fois, au passage à "reçue"
    if payload.status == PurchaseOrderStatus.recue.value and not was_already_received:
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            product.stock_quantity += item.quantity

    db.commit()
    db.refresh(order)
    return order
