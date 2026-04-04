# services/product/app/database.py
# Commerce RDS 연결 설정 및 세션 관리
# DB 접속 정보는 .env에서 로드 (Git에 올리지 말 것)

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")        # commerce.cvoog24wet91.ap-northeast-2.rds.amazonaws.com
DB_PORT     = os.getenv("DB_PORT", 3306)  # 기본값 3306
DB_NAME     = os.getenv("DB_NAME")        # commerce

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

# autocommit=False: 명시적 commit() 필요 / autoflush=False: query 전 자동 flush 방지
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI 의존성 주입용 DB 세션 생성기
    - 요청마다 새 세션 열고 응답 후 반드시 close()
    - 라우터에서 Depends(get_db)로 주입받아 사용
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
