# services/product/app/main.py
# EC2-1 상품 서비스 진입점
# 역할: Commerce RDS에서 상품 목록 조회 후 HTML 렌더링

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app import models
from app.database import get_db, engine  # noqa: F401 - 추후 마이그레이션 시 사용 예정

app = FastAPI()

# Jinja2 템플릿 디렉토리
templates = Jinja2Templates(directory="app/templates")

# /static 경로로 정적 파일 서빙 (배포 시 S3로 대체 예정)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# DB 연결 실패 또는 products 테이블이 비어있을 때 보여줄 임시 상품 데이터
# 주의: item_id 형식(ITEM-00x)이 실제 DB 데이터(beaver_item_0x)와 다름 — 화면 확인용으로만 사용
FALLBACK_PRODUCTS = [
    {"id": 1, "item_id": "ITEM-001", "name": "프리미엄 나뭇가지", "price": 12000, "emoji": "🪵"},
    {"id": 2, "item_id": "ITEM-002", "name": "비버댐 건축 키트", "price": 89000, "emoji": "🏠"},
    {"id": 3, "item_id": "ITEM-003", "name": "댐 공사 안전모", "price": 45000, "emoji": "⛑️"},
    {"id": 4, "item_id": "ITEM-004", "name": "비버 치아 관리 세트", "price": 22000, "emoji": "🦷"},
]


@app.get("/")
async def product_list(request: Request, db: Session = Depends(get_db)):
    """
    메인 상품 목록 페이지
    - Commerce RDS의 products 테이블 전체 조회
    - DB 조회 실패 또는 결과 없으면 FALLBACK_PRODUCTS로 대체
    """
    try:
        db_products = db.query(models.Product).all()
        products_to_show = db_products if db_products else FALLBACK_PRODUCTS
    except Exception as e:
        print(f"⚠️ DB 조회 실패: {e}")
        products_to_show = FALLBACK_PRODUCTS

    return templates.TemplateResponse("main.html", {
        "request": request,
        "products": products_to_show
    })


@app.get("/cart")
async def cart_page(request: Request):
    """
    장바구니 페이지
    - 서버에서 별도 데이터 조회 없음
    - 상품 데이터는 main.html의 addToCart()가 localStorage에 저장한 것을 cart.html JS가 읽어 렌더링
    - TODO: [EC2-4 연동] EC2-4 서버 기동 후 checkout() → POST /api/checkout 실제 동작 확인
    """
    return templates.TemplateResponse("cart.html", {"request": request})


@app.get("/health")
async def health_check():
    """
    서버 상태 확인용 엔드포인트
    - GitHub Actions 배포 후 정상 기동 확인
    - 로드밸런서 헬스체크 경로로도 사용 가능
    """
    return {"status": "ok"}
