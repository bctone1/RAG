from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict


class FileBase(BaseModel):
    original_name: str
    mime_type: str
    storage_path: str


class FileCreate(FileBase):
    pass


class FileRead(FileBase):
    id: int
    uploaded_at: datetime
    model_config = ConfigDict(from_attributes=True)


class DocumentBase(BaseModel):
    file_id: int
    title: str
    doc_meta: Optional[dict[str, Any]] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentRead(DocumentBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ChunkBase(BaseModel):
    document_id: int
    content: str
    chunk_order: int
    chunk_meta: Optional[dict[str, Any]] = None


class ChunkCreate(ChunkBase):
    pass


class ChunkRead(ChunkBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class EmbeddingBase(BaseModel):
    chunk_id: int
    vector: List[float]
    model: str
    dim: int


class EmbeddingCreate(EmbeddingBase):
    pass


class EmbeddingRead(EmbeddingBase):
    model_config = ConfigDict(from_attributes=True)


class ChatHistoryBase(BaseModel):
    user_input: str
    llm_output: str


class ChatHistoryCreate(ChatHistoryBase):
    pass


class ChatHistoryRead(ChatHistoryBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
