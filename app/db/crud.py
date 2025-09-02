from sqlalchemy.orm import Session
from . import models
from app.schemas.db import (
    FileCreate,
    DocumentCreate,
    ChunkCreate,
    EmbeddingCreate,
    ChatLogCreate,
)


def create_file(db: Session, file_in: FileCreate) -> models.File:
    db_obj = models.File(**file_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_file(db: Session, file_id: int) -> models.File | None:
    return db.query(models.File).filter(models.File.id == file_id).first()


def list_files(db: Session) -> list[models.File]:
    return db.query(models.File).all()


def create_document(db: Session, doc_in: DocumentCreate) -> models.Document:
    db_obj = models.Document(**doc_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_document(db: Session, doc_id: int) -> models.Document | None:
    return db.query(models.Document).filter(models.Document.id == doc_id).first()


def list_documents(db: Session) -> list[models.Document]:
    return db.query(models.Document).all()


def create_chunk(db: Session, chunk_in: ChunkCreate) -> models.Chunk:
    db_obj = models.Chunk(**chunk_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def list_chunks_by_document(db: Session, document_id: int) -> list[models.Chunk]:
    return (
        db.query(models.Chunk)
        .filter(models.Chunk.document_id == document_id)
        .order_by(models.Chunk.chunk_order)
        .all()
    )


def create_embedding(db: Session, emb_in: EmbeddingCreate) -> models.Embedding:
    db_obj = models.Embedding(**emb_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_chatlog(db: Session, log_in: ChatLogCreate) -> models.ChatLog:
    db_obj = models.ChatLog(**log_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def list_chatlogs(db: Session) -> list[models.ChatLog]:
    return db.query(models.ChatLog).order_by(models.ChatLog.created_at.desc()).all()
