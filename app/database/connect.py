import asyncio
import logging
import ssl
from os import environ

from decouple import config
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

STAGE = environ.get("STAGE", "local")
DB_NAME = config("DB_NAME").format(STAGE=STAGE)
DB_URL = config("DB_URL").format(DB_NAME=DB_NAME)

class DatabaseInitializer:
    def __init__(self, app: FastAPI = None, **kwargs):
        self.database_name = None
        self.database_url = None
        self._client: AsyncIOMotorClient = None

        if app is not None:
            self.init_app(app=app, *kwargs)

    def init_app(self, app: FastAPI, **kwargs):
        """
        DB 초기화 함수
        :param app: FastAPI 인스턴스
        :param kwargs:
        :return:
        """
        stage = kwargs.get("STAGE", "local")
        self.database_name = config("DB_NAME").format(STAGE=stage)
        self.database_url = config("DB_URL").format(DB_NAME=self.database_name)

        logging.info(f"현재 {STAGE}모드로 실행중입니다.....")
        logging.info(f"{DB_NAME} 데이터베이스에 연결 중입니다.....")
        logging.info(f"{DB_URL} 엔드포인트.....")

        @app.on_event("startup")
        async def startup():
            self._client = AsyncIOMotorClient(self.database_url, ssl_cert_reqs=ssl.CERT_NONE)
            logging.info("DB connected")

        @app.on_event("shutdown")
        async def shutdown():
            self._client.close()
            logging.info("DB disconnected")

    def get_db(self) -> AsyncIOMotorDatabase:
        """
        DB 세션 반환
        :return:
        """
        if self._client is None:
            raise Exception("Must be called 'init_db'")

        db = self._client[self.database_name]
        return db

connection = DatabaseInitializer()