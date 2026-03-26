# 🦫 Beavers Shopping Mall - Payment Service

이 서비스는 Beavers 쇼핑몰의 결제(Checkout)와 사용자 포인트(Wallet) 관리를 담당하는 마이크로서비스입니다.

---

## Tech Stack
* **Framework:** FastAPI
* **Database:** AWS RDS (MySQL)
* **ORM:** SQLAlchemy
* **Validation:** Pydantic (V2)

---

## Folder Structure

* `models/`: DB 테이블 설계도 (`Order`, `Wallet`)
* `routers/`: API 엔드포인트 입구 (`/checkout`, `/wallets`)
* `schemas/`: 데이터 전송 규격 및 유효성 검증 (가격/수량 음수 차단)
* `services/`: 결제 프로세스 및 포인트 연산 핵심 로직
* `database.py`: DB 연결 및 세션 관리

---

## 📡 API Specification

### 1. 지갑(Wallet) 서비스
사용자가 회원가입을 성공하면 아래 API를 호출하여 지갑을 생성

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/wallets/{user_id}` | 신규 유저 지갑 생성 및 **100만 포인트** 지급 |

* **Request Example:** `POST http://localhost:8004/api/wallets/jiwon_01`
* **Response:** `{"status": "success", "balance": 1000000}`

---

### 2. 주문/결제(Order) 서비스
모든 요청은 `http://localhost:8001` (프론트 포트)에서 오는 것을 허용(CORS)하도록 설정되어 있습니다.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/checkout` | 상품 결제 및 주문 생성 (잔액/재고 검증 포함) |
| `GET` | `/api/orders/{user_id}` | 특정 유저의 전체 주문 내역 조회 |
| `PATCH` | `/api/orders/{order_id}` | 주문 취소 및 포인트 환불 처리 |

#### 결제 요청 데이터 예시 (POST `/api/checkout`)
```json
{
  "user_id": "jiwon_test",
  "item_id": "beaver_item_01",
  "price": 50000,
  "quantity": 2
}