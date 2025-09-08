from __future__ import annotations

from pathlib import Path
from typing import List, Tuple
import os
import hashlib
import numpy as np
import fitz  # type: ignore
from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract text from a PDF using PyMuPDF."""
    doc = fitz.open(str(pdf_path))
    texts = [page.get_text() for page in doc]
    doc.close()
    return "\n".join(texts)


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """Split text into chunks using LangChain's RecursiveCharacterTextSplitter."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


def get_embedding(text: str, dim: int = 1536) -> Tuple[List[float], str]:
    """Generate an embedding vector for the given text.

    If an OPENAI_API_KEY is present, use OpenAIEmbeddings via langchain.
    Otherwise, fall back to a deterministic pseudo-random vector so that
    tests can run without external services.
    Returns a tuple of (vector, model_name).
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from langchain_openai import OpenAIEmbeddings

            embeddings = OpenAIEmbeddings(api_key=api_key)
            vec = embeddings.embed_query(text)
            return vec, "openai"
        except Exception:
            pass
    # fallback deterministic vector based on text hash
    h = hashlib.sha256(text.encode("utf-8")).digest()
    rng = np.random.default_rng(int.from_bytes(h[:8], "little"))
    vec = rng.random(dim).tolist()
    return vec, "dummy"