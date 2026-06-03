from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import get_session
from models.ticket import Ticket, TicketCreate, TicketUpdate, TicketRead

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("/", response_model=List[TicketRead])
def get_tickets(
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    query = select(Ticket).order_by(Ticket.created_at.desc())
    tickets = session.exec(query).all()

    if status:
        tickets = [t for t in tickets if t.status == status]
    if category:
        tickets = [t for t in tickets if t.category == category]
    if search:
        s = search.lower()
        tickets = [t for t in tickets if s in t.title.lower() or s in t.description.lower()]

    return tickets

@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: int, session: Session = Depends(get_session)):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.post("/", response_model=TicketRead)
def create_ticket(ticket: TicketCreate, session: Session = Depends(get_session)):
    db_ticket = Ticket.from_orm(ticket)
    session.add(db_ticket)
    session.commit()
    session.refresh(db_ticket)
    return db_ticket

@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket(ticket_id: int, ticket: TicketUpdate, session: Session = Depends(get_session)):
    db_ticket = session.get(Ticket, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    data = ticket.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(db_ticket, k, v)
    db_ticket.updated_at = datetime.utcnow()
    if ticket.status == "resolved" and not db_ticket.resolved_at:
        db_ticket.resolved_at = datetime.utcnow()
    session.add(db_ticket)
    session.commit()
    session.refresh(db_ticket)
    return db_ticket

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, session: Session = Depends(get_session)):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    session.delete(ticket)
    session.commit()
    return {"ok": True}
