from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from .models import Incident

def list_incidents(db: Session) -> list[Incident]:
    return list(db.scalars(select(Incident).options(joinedload(Incident.assignee)).order_by(Incident.id)).all())

def get_incident(db: Session, incident_id: int) -> Incident | None:
    return db.get(Incident, incident_id)
