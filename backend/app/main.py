from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import Base, SessionLocal, engine, get_db
from .models import Employee, Incident
from .schemas import IncidentOut, StatusUpdate
from . import services

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Development-only schema initialization; use Alembic migrations before production.
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.scalar(select(Incident.id).limit(1)) is None:
            alex = Employee(name="Alex Morgan", department="Infrastructure")
            sam = Employee(name="Sam Lee", department="Support")
            db.add_all([alex, sam])
            db.flush()
            db.add_all([
                Incident(title="VPN access intermittent", status="OPEN", priority="HIGH", assignee_id=alex.id),
                Incident(title="Laptop provisioning delay", status="IN_PROGRESS", priority="MEDIUM", assignee_id=sam.id),
                Incident(title="Printer unavailable", status="RESOLVED", priority="LOW")
            ])
            db.commit()
    yield

app = FastAPI(title="Enterprise Operations Portal API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["GET", "PATCH"], allow_headers=["Content-Type"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/incidents", response_model=list[IncidentOut])
def incidents(db: Session = Depends(get_db)):
    return services.list_incidents(db)

@app.patch("/api/incidents/{incident_id}/status", response_model=IncidentOut)
def update_status(incident_id: int, payload: StatusUpdate, db: Session = Depends(get_db)):
    return services.change_status(db, incident_id, payload.status)
