from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import repositories
from .schemas import IncidentOut, Status

def serialize_incident(item) -> IncidentOut:
    return IncidentOut(
        id=item.id, title=item.title, status=item.status,
        priority=item.priority, assigneeName=item.assignee.name if item.assignee else None,
        createdAt=item.created_at
    )

def list_incidents(db: Session) -> list[IncidentOut]:
    return [serialize_incident(item) for item in repositories.list_incidents(db)]

def change_status(db: Session, incident_id: int, status: Status) -> IncidentOut:
    incident = repositories.get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    incident.status = status
    db.commit()
    db.refresh(incident)
    return serialize_incident(incident)
