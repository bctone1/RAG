from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from .base import Base


class File(Base):
    __tablename__ = "file"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(50))
    storage_path: Mapped[str] = mapped_column(String(512), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    documents: Mapped[list[Document]] = relationship(
        back_populates="file", cascade="all, delete-orphan"
    )


class Document(Base):
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    file_id: Mapped[int | None] = mapped_column(
        ForeignKey("file.id", ondelete="CASCADE"),
        nullable=True,
    )
    title: Mapped[str | None] = mapped_column(String(255))
    doc_meta: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    file: Mapped[File | None] = relationship(back_populates="documents")
    chunks: Mapped[list[Chunk]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )


class Chunk(Base):
    __tablename__ = "chunk"
    __table_args__ = (
        UniqueConstraint("document_id", "chunk_order", name="uq_chunk_document_order"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    document_id: Mapped[int | None] = mapped_column(
        ForeignKey("document.id", ondelete="CASCADE"), nullable=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_order: Mapped[int | None] = mapped_column(Integer)
    chunk_meta: Mapped[dict | None] = mapped_column(JSON)

    document: Mapped[Document | None] = relationship(back_populates="chunks")
    embedding: Mapped[Embedding | None] = relationship(
        back_populates="chunk", cascade="all, delete-orphan"
    )


class Embedding(Base):
    __tablename__ = "embedding"

    chunk_id: Mapped[int] = mapped_column(
        ForeignKey("chunk.id", ondelete="CASCADE"),
        primary_key=True,
    )
    vector: Mapped[list[float] | None] = mapped_column(Vector(1536))
    model: Mapped[str | None] = mapped_column(String(100))
    dim: Mapped[int | None] = mapped_column(Integer)

    chunk: Mapped[Chunk | None] = relationship(back_populates="embedding")


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_input: Mapped[str] = mapped_column(Text, nullable=False)
    llm_output: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
