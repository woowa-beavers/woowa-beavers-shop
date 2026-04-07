from fastapi import APIRouter, HTTPException, Response, Form, Depends
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

router = APIRouter()

# 보안 설정
SECRET_KEY = "madi_super_secret_key" # 실제 운영시 환경변수로 관리
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 임시 인메모리 DB (테스트용)
fake_users_db = {}

@router.post("/signup")
async def signup(username: str = Form(...), password: str = Form(...)):
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")
    
    hashed_password = pwd_context.hash(password)
    fake_users_db[username] = {"username": username, "password": hashed_password}
    return {"message": "회원가입 성공"}

@router.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    user = fake_users_db.get(username)
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸습니다.")

    # JWT 토큰 생성
    expire = datetime.utcnow() + timedelta(hours=24)
    token = jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

    # 쿠키에 토큰 저장 (HttpOnly로 XSS 방어)
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {token}", 
        httponly=True,
        samesite="lax"
    )
    return {"message": "로그인 성공"}