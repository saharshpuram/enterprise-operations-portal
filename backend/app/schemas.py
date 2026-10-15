from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict

Status = Literal["OPEN", "IN_PROGRESS", "RESOLVED"]

class StatusUpdate(BaseModel):
    status: Status

class IncidentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    status: str
    priority: str
    assigneeName: str | None
    createdAt: datetime
