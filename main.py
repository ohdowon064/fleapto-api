from os import environ, getenv

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from mangum import Mangum
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.database.connect import Mongo

from app.middleware.token_validator import access_control

from app.router import index, auth, users, products, history

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)

def create_app():
    """
    앱 함수 실행
    :return:
    """
    STAGE = environ.get("STAGE", "local")
    ROOT_PATH = f"/{STAGE}" if STAGE and STAGE != "local" else ""

    # 앱 생성
    app = FastAPI(title="Fleato API", root_path=ROOT_PATH)

    # 데이터베이스 초기화
    app.add_event_handler("shutdown", Mongo.disconnected_db)

    # 미들웨어 정의
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"], except_path=["/health"])

    # 라우터 정의
    app.include_router(index.router, tags=["Root"])
    app.include_router(auth.router, tags=["Authentication"], prefix="/api")
    app.include_router(users.router, tags=["Users"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])
    app.include_router(products.router, tags=["Products"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])
    app.include_router(history.router, tags=["history"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])

    return app

app = create_app()
handler = Mangum(app)

if __name__ == "__main__":
    print("환경변수 출력")
    print(getenv("STAGE"))
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)