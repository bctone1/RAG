# app/api/v1/auth.py
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(body: dict):
    return {"ok": True}