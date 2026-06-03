from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class InfrastructureBase(SQLModel):
    name: str
    type: str = "other"     # server | switch | firewall | router | ap | other
    ip_range: str = ""
    os_version: str = ""
    services: str = ""      # e.g. "DNS, DHCP, AD"
    location: str = ""
    notes: str = ""         # markdown supported

class Infrastructure(InfrastructureBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class InfrastructureCreate(InfrastructureBase):
    pass

class InfrastructureUpdate(SQLModel):
    name: Optional[str] = None
    type: Optional[str] = None
    ip_range: Optional[str] = None
    os_version: Optional[str] = None
    services: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class InfrastructureRead(InfrastructureBase):
    id: int
    created_at: datetime
    updated_at: datetime
