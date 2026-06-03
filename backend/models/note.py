from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class NoteBase(SQLModel):
    title: str
    body: str = ""
    tags: str = ""          # comma-separated e.g. "networking,vlan,week1"
    is_quick: bool = False  # True = quick capture, False = full note
    linked_ticket_id: Optional[int] = Field(default=None, foreign_key="ticket.id")
    linked_device_id: Optional[int] = Field(default=None, foreign_key="device.id")

class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class NoteCreate(NoteBase):
    pass

class NoteUpdate(SQLModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[str] = None
    is_quick: Optional[bool] = None
    linked_ticket_id: Optional[int] = None
    linked_device_id: Optional[int] = None

class NoteRead(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime
