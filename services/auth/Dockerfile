FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 실행 명령어
CMD ["uvicorn", "services.auth.app.main:app", "--host", "0.0.0.0", "--port", "8000"]