"""대화 로그 엔드포인트"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.schemas.db import ChatLogCreate, ChatLogRead

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/logs", response_model=ChatLogRead)
def create_log(log: ChatLogCreate, db: Session = Depends(get_db)):
    return crud.create_chatlog(db, log)


@router.get("/logs", response_model=list[ChatLogRead])
def list_logs(db: Session = Depends(get_db)):
    return crud.list_chatlogs(db)
