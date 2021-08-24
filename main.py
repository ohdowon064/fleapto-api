import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.router import index, auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(index.router, tags=["Root"])
app.include_router(auth.router, tags=["Users"], prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port="8000", reload=True)
