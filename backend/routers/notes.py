from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import get_session
from models.note import Note, NoteCreate, NoteUpdate, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/", response_model=List[NoteRead])
def get_notes(
    search: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    query = select(Note).order_by(Note.updated_at.desc())
    notes = session.exec(query).all()

    if search:
        s = search.lower()
        notes = [n for n in notes if s in n.title.lower() or s in n.body.lower()]
    if tag:
        notes = [n for n in notes if tag.lower() in n.tags.lower()]

    return notes

@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("/", response_model=NoteRead)
def create_note(note: NoteCreate, session: Session = Depends(get_session)):
    db_note = Note.from_orm(note)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note

@router.patch("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, note: NoteUpdate, session: Session = Depends(get_session)):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    data = note.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(db_note, k, v)
    db_note.updated_at = datetime.utcnow()
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note

@router.delete("/{note_id}")
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return {"ok": True}
