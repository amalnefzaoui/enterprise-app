from datetime import date as date_type, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.attendance import Attendance, AttendanceStatus
from app.schemas.attendance import AttendanceAction, AttendanceOut
from app.auth.dependencies import get_current_user
from app.schemas.auth import CurrentUser

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


@router.post("/checkin", response_model=AttendanceOut, status_code=201)
def check_in(payload: AttendanceAction, db: Session = Depends(get_db)):
    today = date_type.today()
    now = datetime.now().time()

    existing = db.query(Attendance).filter(
        Attendance.employee_id == payload.employee_id,
        Attendance.date == today,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Déjà pointé aujourd'hui")

    # Retard si arrivée après 09h15 (règle métier configurable)
    status_value = AttendanceStatus.retard if now.strftime("%H:%M:%S") > "09:15:00" else AttendanceStatus.present

    record = Attendance(
        employee_id=payload.employee_id,
        date=today,
        check_in=now,
        status=status_value,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.post("/checkout", response_model=AttendanceOut)
def check_out(payload: AttendanceAction, db: Session = Depends(get_db)):
    today = date_type.today()
    record = db.query(Attendance).filter(
        Attendance.employee_id == payload.employee_id,
        Attendance.date == today,
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Aucun pointage d'entrée trouvé")

    record.check_out = datetime.now().time()
    db.commit()
    db.refresh(record)
    return record


@router.get("/report", response_model=list[AttendanceOut])
def attendance_report(
    employee_id: int | None = None,
    month: int | None = None,
    year: int | None = None,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    today = date_type.today()
    y = year or today.year
    m = month or today.month

    from calendar import monthrange
    last_day = monthrange(y, m)[1]
    start = date_type(y, m, 1)
    end = date_type(y, m, last_day)

    query = db.query(Attendance).filter(Attendance.date.between(start, end))

    if current_user.role == "employee":
        if not current_user.employee_id:
            return []
        query = query.filter(Attendance.employee_id == current_user.employee_id)
    elif employee_id:
        query = query.filter(Attendance.employee_id == employee_id)

    return query.order_by(Attendance.date.asc()).all()
    