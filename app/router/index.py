from datetime import datetime

from fastapi import APIRouter, status, Response, Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates

from app.database.connect import Mongo
from app.utils.data_utils import InitDB

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    url = request.url
    print(f"url::::::::{url}")
    current_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>Fleapto Time</title>
    </head>
    <body>
        <h1>Fleapto API Server Time</h1>
        <h2 id="clock" style="color:black;">clock</h1>

        <script>
            var Target = document.getElementById("clock");
            function clock() {
                var time = new Date();

                var month = time.getMonth();
                var date = time.getDate();
                var day = time.getDay();
                var week = ['일', '월', '화', '수', '목', '금', '토'];

                var hours = time.getHours();
                var minutes = time.getMinutes();
                var seconds = time.getSeconds();

                Target.innerText =
                `KST ${month + 1}월 ${date}일 ${week[day]}요일 ` +
                `${hours < 10 ? `0${hours}` : hours}:${minutes < 10 ? `0${minutes}` : minutes}:${seconds < 10 ? `0${seconds}` : seconds}`;

            }
            clock();
            setInterval(clock, 1000); // 1초마다 실행
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=current_html, status_code=200)


@router.delete("/init")
async def init():
    await InitDB().init_db()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(msg="데이터베이스를 초기화했습니다.")
    )