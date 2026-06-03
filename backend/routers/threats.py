from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from database import get_session
from models.threat import ThreatItem, ThreatItemRead

router = APIRouter(prefix="/threats", tags=["threats"])

@router.get("/", response_model=List[ThreatItemRead])
def get_threats(
    relevant_only: bool = Query(False),
    severity: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    items = session.exec(
        select(ThreatItem).order_by(ThreatItem.published_at.desc())
    ).all()
    if relevant_only:
        items = [i for i in items if i.relevant]
    if severity:
        items = [i for i in items if i.severity == severity.upper()]
    if source:
        items = [i for i in items if i.source == source.upper()]
    return items
