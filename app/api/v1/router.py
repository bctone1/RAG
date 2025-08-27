from fastapi import APIRouter
from . import auth, files, rag, chat, admin, test,test_ingestion
from ...services import ingestion


# router = APIRouter(prefix="/v1")
router = APIRouter()
for r in (auth, files, rag, chat, admin,test,test_ingestion):
    router.include_router(r.router)

# router = APIRouter(prefix="/v1")
# router.include_router(test.test_router)


# from app.api.v1.test_ingestion import router as ingestion
# router.include_router(ingestion, prefix="/api/v1")