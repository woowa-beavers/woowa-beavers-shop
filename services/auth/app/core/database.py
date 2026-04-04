import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. .env 파일 로드
load_dotenv()

# 2. 환경 변수에서 URL 가져오기 (없으면 sqlite 폴백)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# 3. 엔진 생성
engine = create_engine(DATABASE_URL)

# 4. 세션 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Base 클래스 생성 (모델들이 이를 상속받음)
Base = declarative_base()

# 6. DB 세션을 생성하고 반환하는 의존성 주입 함수 (FastAPI 기준)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()