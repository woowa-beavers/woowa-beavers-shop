import os
from fastapi import FastAPI, Request, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from jose import jwt, JWTError # auth_router에서 사용하는 jose 라이브러리 추가

from services.auth.app.routers import auth_router
from services.auth.app.routers.auth_router import SECRET_KEY, ALGORITHM # 라우터에 선언된 키와 알고리즘 가져오기
from services.auth.app.core.database import engine
from services.auth.app.models.user import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service", root_path="/api")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ---------------------------
# 웹 페이지용 JWT 검증 함수 (디버그 로그 추가)
# ---------------------------
async def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    print(f"🚨 [디버그] 1. 쿠키에서 꺼낸 토큰: {token}")
    
    # 쿠키가 없으면 None 반환
    if not token:
        print("🚨 [디버그] 2. 브라우저가 쿠키를 안 보냈습니다!")
        return None
        
    token = token.replace("Bearer ", "")
    
    try:
        # 토큰 검증
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"🚨 [디버그] 3. 토큰 정상 해독 완료! 접속 유저: {payload.get('sub')}")
        return payload.get("sub")
    except JWTError as e:
        # 토큰이 만료되었거나 변조되었다면 None 반환
        print(f"🚨 [디버그] 4. 토큰 해독 실패 (비밀키가 다르거나 깨짐) 에러: {e}")
        return None

@app.get("/")
async def root():
    # 💡 HTTPS 깨짐/무한 리다이렉트 방지를 위해 302 상태 코드 추가 완료!
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@app.get("/login")
async def login_page(request: Request):
    # 명시적 파라미터 지정으로 TypeError(unhashable type: 'dict') 해결
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/signup")
async def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html")

@app.get("/main")
async def main_page(request: Request, user: str | None = Depends(get_current_user_from_cookie)):
    # 유효한 유저 정보가 없으면 로그인 페이지로 강제 이동 (401 에러 대신 Redirect)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
    return templates.TemplateResponse(request=request, name="index.html")

app.include_router(auth_router.router, prefix="/api/auth")