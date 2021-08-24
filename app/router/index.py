from datetime import datetime

from fastapi import APIRouter, status, Response

router = APIRouter()

@router.get("/")
async def index():
    current_time = datetime.utcnow()
    return Response(f"Fleapto API (UTC : {current_time.strftime('%Y.%m.%d %H:%M:%S')})", media_type="text/plain")
