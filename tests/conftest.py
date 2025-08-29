import os

# pytest 실행 시 전역 적용
os.environ["DEBUG"] = "true"
os.environ["UPLOAD_FOLDER"] = "./tmp"
