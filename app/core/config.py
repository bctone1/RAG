import os
from dotenv import load_dotenv


# ==============================================================
# 환경변수 로드
# ==============================================================
load_dotenv(override=True)  # .env 파일 로드

# ==============================================================
# 경로(BASE_DIR, 업로드 폴더)
# ==============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "file", "upload")

