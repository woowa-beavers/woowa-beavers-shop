# 베이스 이미지
FROM python:3.9-slim

# 작업 폴더 설정
WORKDIR /app

# 준비물 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사: app 폴더(main.py, router 등)를 통째로 컨테이너 안으로 복사한다.
COPY . .

# 실행 명령어
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]