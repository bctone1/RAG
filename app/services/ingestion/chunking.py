"""텍스트를 일정 길이로 청크 단위로 나누는 모듈."""
from __future__ import annotations
from typing import List, Dict

def chunk_text(text: str, size: int = 500) -> List[Dict[str, str]]:
    """주어진 텍스트를 ``size`` 길이의 조각으로 나눈다.
    각 조각은 순서를 보존하기 위해 ``order`` 필드와 ``text`` 필드를 가진다.
    ``order``는 1부터 시작한다.

    Args:
        text: 분할할 원본 문자열.
        size: 각 청크의 최대 길이.

    Returns:
        order와 text를 담은 사전의 리스트.
    """
    chunks: List[Dict[str, str]] = []
    for idx, start in enumerate(range(0, len(text), size), start=1):
        chunk = text[start : start + size]
        chunks.append({"order": idx, "text": chunk})
    return chunks
