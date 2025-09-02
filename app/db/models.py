from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from .base import Base


class File(Base):
    __tablename__ = "files"

    id = Column(BigInteger, primary_key=True, index=True)
    original_name = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    documents = relationship("Document", back_populates="file")


class Document(Base):
    __tablename__ = "documents"

    id = Column(BigInteger, primary_key=True, index=True)
    file_id = Column(BigInteger, ForeignKey("files.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    doc_meta = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    file = relationship("File", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document")


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(BigInteger, primary_key=True, index=True)
    document_id = Column(BigInteger, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    chunk_order = Column(Integer, nullable=False)
    chunk_meta = Column(JSONB, nullable=True)

    document = relationship("Document", back_populates="chunks")
    embedding = relationship("Embedding", uselist=False, back_populates="chunk")


class Embedding(Base):
    __tablename__ = "embeddings"

    chunk_id = Column(BigInteger, ForeignKey("chunks.id", ondelete="CASCADE"), primary_key=True)
    vector = Column(Vector(), nullable=False)
    model = Column(String, nullable=False)
    dim = Column(Integer, nullable=False)

    chunk = relationship("Chunk", back_populates="embedding")


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    llm_output = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
