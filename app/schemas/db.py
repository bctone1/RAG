from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel


class FileBase(BaseModel):
    original_name: str
    mime_type: str
    storage_path: str


class FileCreate(FileBase):
    pass


class FileRead(FileBase):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True


class DocumentBase(BaseModel):
    file_id: int
    title: str
    doc_meta: Optional[dict[str, Any]] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentRead(DocumentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ChunkBase(BaseModel):
    document_id: int
    content: str
    chunk_order: int
    chunk_meta: Optional[dict[str, Any]] = None


class ChunkCreate(ChunkBase):
    pass


class ChunkRead(ChunkBase):
    id: int

    class Config:
        orm_mode = True


class EmbeddingBase(BaseModel):
    chunk_id: int
    vector: List[float]
    model: str
    dim: int


class EmbeddingCreate(EmbeddingBase):
    pass


class EmbeddingRead(EmbeddingBase):
    class Config:
        orm_mode = True


class ChatHistoryBase(BaseModel):
    user_input: str
    llm_output: str


class ChatHistoryCreate(ChatHistoryBase):
    pass


class ChatHistoryRead(ChatHistoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
