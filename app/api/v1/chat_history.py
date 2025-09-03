"""대화 히스토리 엔드포인트"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.schemas.db import ChatHistoryCreate, ChatHistoryRead

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/history", response_model=ChatHistoryRead)
def create_history(log: ChatHistoryCreate, db: Session = Depends(get_db)):
    return crud.create_chathistory(db, log)


@router.get("/history", response_model=list[ChatHistoryRead])
def list_history(db: Session = Depends(get_db)):
    return crud.list_chathistory(db)
