from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.leave import Leave, LeaveType, LeaveStatus
from app.models.employee import Employee
from app.schemas.leave import LeaveCreate, LeaveStatusUpdate, LeaveOut
from app.auth.dependencies import require_role

router = APIRouter(prefix="/api/leaves", tags=["leaves"])


def calculate_business_days(start, end) -> int:
    """Calcule le nombre de jours ouvrés entre deux dates (hors weekends)."""
    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:  # 0=lundi ... 4=vendredi
            count += 1
        current += timedelta(days=1)
    return count


@router.get("/", response_model=list[LeaveOut])
def list_leaves(
    status_filter: str | None = None,
    employee_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Leave)
    if status_filter:
        query = query.filter(Leave.status == status_filter)
    if employee_id:
        query = query.filter(Leave.employee_id == employee_id)
    return query.order_by(Leave.created_at.desc()).all()


@router.post("/", response_model=LeaveOut, status_code=status.HTTP_201_CREATED)
def create_leave(payload: LeaveCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == payload.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employé non trouvé")

    days_count = calculate_business_days(payload.start_date, payload.end_date)

    if payload.type == LeaveType.conge_paye and employee.leave_balance < days_count:
        raise HTTPException(status_code=400, detail="Solde de congés insuffisant")

    leave = Leave(
        employee_id=payload.employee_id,
        type=payload.type,
        start_date=payload.start_date,
        end_date=payload.end_date,
        days_count=days_count,
        reason=payload.reason,
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave


@router.patch("/{leave_id}/status", response_model=LeaveOut)
def update_leave_status(
    leave_id: int,
    payload: LeaveStatusUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_role("admin", "manager")),
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Demande non trouvée")

    leave.status = payload.status
    leave.approved_by = payload.approved_by

    if payload.status == LeaveStatus.approuve and leave.type == LeaveType.conge_paye:
        employee = db.query(Employee).filter(Employee.id == leave.employee_id).first()
        employee.leave_balance -= leave.days_count

    db.commit()
    db.refresh(leave)
    return leave
