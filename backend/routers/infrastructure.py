from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import get_session
from models.infrastructure import Infrastructure, InfrastructureCreate, InfrastructureUpdate, InfrastructureRead

router = APIRouter(prefix="/infrastructure", tags=["infrastructure"])

@router.get("/", response_model=List[InfrastructureRead])
def get_infra(
    type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    items = session.exec(select(Infrastructure).order_by(Infrastructure.name)).all()
    if type:
        items = [i for i in items if i.type == type]
    if search:
        s = search.lower()
        items = [i for i in items if s in i.name.lower() or s in i.notes.lower()]
    return items

@router.get("/{item_id}", response_model=InfrastructureRead)
def get_infra_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Infrastructure, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", response_model=InfrastructureRead)
def create_infra(item: InfrastructureCreate, session: Session = Depends(get_session)):
    db_item = Infrastructure.from_orm(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.patch("/{item_id}", response_model=InfrastructureRead)
def update_infra(item_id: int, item: InfrastructureUpdate, session: Session = Depends(get_session)):
    db_item = session.get(Infrastructure, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    data = item.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(db_item, k, v)
    db_item.updated_at = datetime.utcnow()
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_infra(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Infrastructure, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
