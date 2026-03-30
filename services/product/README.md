# EC2-1 상품 서비스 (Product Service)

상품 목록 조회 및 장바구니 기능을 담당하는 서비스입니다.

---

## 기술 스택

| 항목 | 내용 |
|------|------|
| Framework | FastAPI (Python 3.11) |
| Template | Jinja2 |
| ORM | SQLAlchemy + PyMySQL |
| DB | Commerce RDS (MySQL, 읽기 전용) |
| 배포 | Docker, EC2-1 Public (43.203.169.11) |

---

## API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | `/` | 상품 목록 페이지 (main.html 렌더링) |
| GET | `/cart` | 장바구니 페이지 (cart.html 렌더링) |
| GET | `/health` | 서버 상태 확인 |

---

## 로컬 실행 방법

### 1. 환경 변수 설정

`services/product/.env` 파일 생성 (Git 미포함, 직접 작성):

```env
DB_USER=admin
DB_PASSWORD=<비밀번호>
DB_HOST=commerce.cvoog24wet91.ap-northeast-2.rds.amazonaws.com
DB_PORT=3306
DB_NAME=commerce
```

### 2. Docker로 실행

```bash
cd services/product
docker build -t beaver-product .
docker run -d -p 8000:8000 --env-file .env --restart always --name beaver-product beaver-product
```

### 3. 동작 확인

```bash
curl http://localhost/health
# {"status": "ok"}
```

브라우저에서 `http://localhost` 접속

---

## 배포 주소

| 환경 | URL |
|------|-----|
| 운영 | https://woowabeavers.cloud |
| 로컬 | http://localhost:8000 |

---

## DB 구성

Commerce RDS의 `products` 테이블을 읽기 전용으로 사용합니다.

```sql
CREATE TABLE products (
    id      INT PRIMARY KEY AUTO_INCREMENT,
    item_id VARCHAR(50) UNIQUE NOT NULL,  -- 예: beaver_item_01
    name    VARCHAR(100) NOT NULL,
    price   INT NOT NULL,
    emoji   VARCHAR(20)
) CHARACTER SET utf8mb4;
```

> DB 조회 실패 시 `main.py`의 `FALLBACK_PRODUCTS`로 자동 대체됩니다.

---

## 장바구니 동작 방식

서버 상태를 사용하지 않고 브라우저 `localStorage`에 저장합니다.

```
저장 키: beaver_cart
저장 형식: [{ itemId, name, price, emoji, quantity }, ...]
```

결제 시 `cart.html`의 `checkout()` 함수가 API Gateway를 통해 EC2-4로 요청을 전송합니다.

```
POST https://c9muocyrwc.execute-api.ap-northeast-2.amazonaws.com/api/checkout
{ user_id, item_id, price, quantity }
```

---

## 타 서비스 연동 현황

| 서비스 | 상태 | 연동 내용 | 담당 |
|--------|------|-----------|------|
| EC2-2 (로그인) | ⏳ 대기 | 헤더 로그인 링크, checkout() user_id 실제 값으로 교체 | EC2-2 담당자 |
| EC2-4 (결제) | ⏳ 대기 | API Gateway CORS 도메인 추가, EC2-4 Docker 기동 | EC2-4 담당자 |
| EC2-3 (재고) | ⏳ 대기 | EC2-4 MOCK_INVENTORY → EC2-3 실제 재고 API 연동 | EC2-3, EC2-4 담당자 |

EC2-2 연동 완료 시 수정할 파일:
- `app/templates/main.html` — 헤더 로그인 링크 (TODO 주석 참고)
- `app/templates/cart.html` — `checkout()` 내 `userId` (TODO 주석 참고)
