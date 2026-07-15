from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import *  # noqa: F401,F403 — assure l'enregistrement de tous les modèles

from app.routers import (
    auth,
    employees,
    leaves,
    attendance,
    products,
    suppliers,
    customers,
    purchase_orders,
    sales_orders,
    invoices,
)

app = FastAPI(
    title="Enterprise API — RH & Achat/Vente",
    description="API Python (FastAPI) pour la gestion RH et Achat/Vente",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Création des tables au démarrage (approche simple ; migrations Alembic recommandées en prod)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(leaves.router)
app.include_router(attendance.router)
app.include_router(products.router)
app.include_router(suppliers.router)
app.include_router(customers.router)
app.include_router(purchase_orders.router)
app.include_router(sales_orders.router)
app.include_router(invoices.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Python API opérationnelle"}
