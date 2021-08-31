from os import environ

import uvicorn
from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.database.connect import connection
from app.middleware.token_validator import access_control
from app.router import index, auth

def created_app():
    """
    앱 함수 실행
    :return:
    """

    # 환경변수 체크
    STAGE = environ.get("STAGE", "local")
    root_path = f"/{STAGE}" if STAGE and STAGE != "local" else "/"

    # 앱 생성
    app = FastAPI(title="Fleato API", root_path=root_path)

    # 데이터베이스 초기화
    connection.init_app(app, STAGE=STAGE)

    # 미들웨어 정의
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 정의
    app.include_router(index.router, tags=["Root"])
    app.include_router(auth.router, tags=["Users"], prefix="/api")

    return app


app = created_app()
handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port="8000", reload=True)
