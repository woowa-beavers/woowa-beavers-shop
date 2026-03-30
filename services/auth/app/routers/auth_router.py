import httpx  # 지갑 서버 통신을 위한 라이브러리

from fastapi import APIRouter, HTTPException, Response, Form, Request, Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError

# DB 연결 함수와 User 모델 불러오기
from services.auth.app.core.database import get_db 
from services.auth.app.models.user import User
from services.auth.app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

SECRET_KEY = "this-is-super-secure-secret-key-at-least-32-bytes-long"
ALGORITHM = "HS256"

@router.post("/signup")
async def signup(
    username: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db) 
):
    # 1. DB에서 이미 존재하는 아이디인지 검색
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")

    # 2. 새로운 유저 객체 생성 (비밀번호는 해싱 처리)
    new_user = User(
        username=username,
        password=hash_password(password)
    )

    # 3. DB에 저장
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 4. [지갑 생성 연동] 지갑 서버 호출
    try:
        async with httpx.AsyncClient() as client:
            wallet_url = f"http://10.0.2.74:8000/api/wallets/{username}"
            await client.post(wallet_url)
    except Exception as e:
        print(f"지갑 생성 중 통신 에러 발생: {e}")

    return {"status": "success"}


@router.post("/login")
async def login(
    response: Response, 
    username: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db) 
):
    # 1. DB에서 유저 정보 가져오기
    user = db.query(User).filter(User.username == username).first()

    # 2. 유저가 없거나 비밀번호가 틀렸을 때 예외 처리
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸습니다.")

    # 3. 토큰 발급 및 쿠키 저장
    token = create_access_token({"sub": username})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True
    )

    return {"status": "success"}


def verify_token(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="로그인 필요")

    token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰")


@router.get("/me")
def get_me(user_payload=Depends(verify_token), db: Session = Depends(get_db)):
    # 토큰의 유저가 DB에 존재하는지 검증
    user = db.query(User).filter(User.username == user_payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
        
    return {"username": user.username, "user_id": user.id}