"""문서 및 청크 CRUD 엔드포인트"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.schemas.db import (
    DocumentCreate,
    DocumentRead,
    ChunkCreate,
    ChunkRead,
)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/", response_model=DocumentRead)
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    if not crud.get_file(db, document.file_id):
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다")
    return crud.create_document(db, document)


@router.get("/{doc_id}", response_model=DocumentRead)
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = crud.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다")
    return doc


@router.get("/", response_model=list[DocumentRead])
def list_documents(db: Session = Depends(get_db)):
    return crud.list_documents(db)


@router.post("/{doc_id}/chunks", response_model=ChunkRead)
def add_chunk(doc_id: int, chunk: ChunkCreate, db: Session = Depends(get_db)):
    if doc_id != chunk.document_id:
        raise HTTPException(status_code=400, detail="문서 ID 불일치")
    if not crud.get_document(db, doc_id):
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다")
    return crud.create_chunk(db, chunk)


@router.get("/{doc_id}/chunks", response_model=list[ChunkRead])
def list_chunks(doc_id: int, db: Session = Depends(get_db)):
    if not crud.get_document(db, doc_id):
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다")
    return crud.list_chunks_by_document(db, doc_id)
