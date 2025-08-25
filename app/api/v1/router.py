from fastapi import APIRouter
from . import auth, files, rag, chat, admin, test

router = APIRouter(prefix="/v1")
for r in (auth, files, rag, chat, admin,test):
    router.include_router(r.router)

# router = APIRouter(prefix="/v1")
# router.include_router(test.test_router)

