from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class ThreatItemBase(SQLModel):
    source: str                     # CISA | NVD | OTX
    external_id: str = ""           # CVE-2024-XXXX or CISA alert ID
    title: str
    severity: str = "MEDIUM"        # CRITICAL | HIGH | MEDIUM | LOW
    affected_products: str = "[]"   # JSON array stored as string
    relevant: bool = False          # agent-scored against inventory
    agent_summary: str = ""         # plain-English impact for your env
    url: str = ""
    published_at: Optional[datetime] = None

class ThreatItem(ThreatItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fetched_at: datetime = Field(default_factory=datetime.utcnow)

class ThreatItemRead(ThreatItemBase):
    id: int
    fetched_at: datetime
