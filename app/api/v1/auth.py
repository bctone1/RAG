# app/api/v1/auth.py
from fastapi import APIRouter, HTTPException, status
import os
import time
import json
import hmac
import hashlib
import base64

router = APIRouter(prefix="/auth", tags=["auth"])

def _b64(data: bytes) -> str:
    """JWT에서 사용하는 base64url 인코딩."""
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _create_jwt(username: str, secret: str, expire_min: int) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": username, "exp": int(time.time()) + expire_min * 60}
    header_b64 = _b64(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = _b64(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature = _b64(hmac.new(secret.encode(), signing_input, hashlib.sha256).digest())
    return f"{header_b64}.{payload_b64}.{signature}"



@router.post("/login")
def login(body: dict):
    # return {"ok": True}
    username = body.get("username")
    password = body.get("password")
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username과 password가 필요합니다.",
        )

    expected_user = os.getenv("ADMIN_USERNAME")
    expected_pass = os.getenv("ADMIN_PASSWORD")
    if expected_user is None or expected_pass is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="인증 정보가 설정되지 않았습니다.",
        )

    if username != expected_user or password != expected_pass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 자격 증명입니다.",
        )

    secret = os.getenv("JWT_SECRET")
    expire = int(os.getenv("ACCESS_TOKEN_EXPIRE_MIN", "60"))

    if secret:
        token = _create_jwt(username, secret, expire)
        return {"access_token": token, "token_type": "bearer"}

    return {"session": {"user": username}}
