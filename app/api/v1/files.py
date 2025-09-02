"""파일 관련 CRUD 엔드포인트"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.schemas.db import FileCreate, FileRead

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/", response_model=FileRead)
def create_file(file: FileCreate, db: Session = Depends(get_db)):
    return crud.create_file(db, file)


@router.get("/{file_id}", response_model=FileRead)
def get_file(file_id: int, db: Session = Depends(get_db)):
    db_file = crud.get_file(db, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다")
    return db_file


@router.get("/", response_model=list[FileRead])
def list_files(db: Session = Depends(get_db)):
    return crud.list_files(db)
