from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class TicketBase(SQLModel):
    title: str
    description: str = ""
    category: str = "general"   # hw | sw | network | account | general
    status: str = "open"        # open | wip | resolved
    priority: str = "medium"    # low | medium | high | critical
    steps_tried: str = ""
    resolution: str = ""
    device_id: Optional[int] = Field(default=None, foreign_key="device.id")

class Ticket(TicketBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None

class TicketCreate(TicketBase):
    pass

class TicketUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    steps_tried: Optional[str] = None
    resolution: Optional[str] = None
    device_id: Optional[int] = None
    resolved_at: Optional[datetime] = None

class TicketRead(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
