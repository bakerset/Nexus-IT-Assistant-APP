from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_session
from agent.nexus_agent import chat
from agent.nudges import get_nudges

router = APIRouter(prefix="/agent", tags=["agent"])

class ChatMessage(BaseModel):
    message: str
    history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
def agent_chat(payload: ChatMessage):
    response = chat(payload.message, payload.history)
    return {"response": response}

@router.get("/nudges")
def agent_nudges(session: Session = Depends(get_session)):
    return get_nudges(session)
