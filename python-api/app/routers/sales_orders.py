from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.sales_order import SalesOrder, SalesOrderItem, SalesOrderStatus
from app.models.product import Product
from app.schemas.orders import SalesOrderCreate, SalesOrderOut, OrderStatusUpdate
from app.auth.dependencies import require_role

router = APIRouter(prefix="/api/sales-orders", tags=["sales-orders"])


@router.get("/", response_model=list[SalesOrderOut])
def list_sales_orders(
    status_filter: str | None = None,
    customer_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(SalesOrder).options(joinedload(SalesOrder.items))
    if status_filter:
        query = query.filter(SalesOrder.status == status_filter)
    if customer_id:
        query = query.filter(SalesOrder.customer_id == customer_id)
    return query.order_by(SalesOrder.created_at.desc()).all()


@router.get("/{order_id}", response_model=SalesOrderOut)
def get_sales_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(SalesOrder).options(joinedload(SalesOrder.items)).filter(
        SalesOrder.id == order_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order


@router.post("/", response_model=SalesOrderOut, status_code=status.HTTP_201_CREATED)
def create_sales_order(payload: SalesOrderCreate, db: Session = Depends(get_db)):
    if not payload.items:
        raise HTTPException(status_code=400, detail="La commande doit contenir au moins un produit")

    # Vérification du stock disponible avant de créer la commande
    for item in payload.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produit {item.product_id} introuvable")
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuffisant pour \"{product.name}\" (disponible: {product.stock_quantity})",
            )

    total_amount = sum(item.quantity * item.unit_price for item in payload.items)

    order = SalesOrder(
        customer_id=payload.customer_id,
        total_amount=total_amount,
        status=SalesOrderStatus.brouillon,
    )
    db.add(order)
    db.flush()

    for item in payload.items:
        db.add(SalesOrderItem(
            sales_order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.quantity * item.unit_price,
        ))

    db.commit()
    db.refresh(order)
    return order


@router.patch("/{order_id}/status", response_model=SalesOrderOut)
def update_sales_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_role("admin", "manager")),
):
    order = db.query(SalesOrder).options(joinedload(SalesOrder.items)).filter(
        SalesOrder.id == order_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    was_already_confirmed = order.status in (SalesOrderStatus.confirmee, SalesOrderStatus.livree)

    if payload.status == SalesOrderStatus.confirmee.value and not was_already_confirmed:
        # Re-vérification du stock au moment de la confirmation
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product.stock_quantity < item.quantity:
                raise HTTPException(status_code=400, detail=f"Stock insuffisant pour \"{product.name}\"")

        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            product.stock_quantity -= item.quantity

    order.status = payload.status
    db.commit()
    db.refresh(order)
    return order
