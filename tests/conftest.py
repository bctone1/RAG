import os
import sys
from pathlib import Path

# 프로젝트 루트를 모듈 탐색 경로에 추가
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# pytest 실행 시 전역 적용
os.environ["DEBUG"] = "true"
os.environ["UPLOAD_FOLDER"] = "./tmp"
