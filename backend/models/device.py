from typing import Optional
from datetime import datetime, date
from sqlmodel import Field, SQLModel

class DeviceBase(SQLModel):
    hostname: str
    user_name: str = ""
    os: str = ""            # e.g. "Windows 10 22H2"
    cpu: str = ""
    ram_gb: int = 0
    gpu: str = ""
    disk_gb: int = 0
    patch_level: str = ""
    av_installed: bool = False
    encrypted: bool = False
    eol_date: Optional[date] = None
    notes: str = ""

class Device(DeviceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(SQLModel):
    hostname: Optional[str] = None
    user_name: Optional[str] = None
    os: Optional[str] = None
    cpu: Optional[str] = None
    ram_gb: Optional[int] = None
    gpu: Optional[str] = None
    disk_gb: Optional[int] = None
    patch_level: Optional[str] = None
    av_installed: Optional[bool] = None
    encrypted: Optional[bool] = None
    eol_date: Optional[date] = None
    notes: Optional[str] = None

class DeviceRead(DeviceBase):
    id: int
    created_at: datetime
    updated_at: datetime
