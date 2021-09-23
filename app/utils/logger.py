import json
import logging
import traceback
from time import time

from fastapi.logger import logger
from fastapi.requests import Request

from app.utils.date_utils import D

logger.setLevel(logging.INFO)

async def api_logger(request: Request, response=None, error=None):
    t = time() - request.state.start
    status_code = error.status_code if error else response.status_code
    error_detail = None
    user = request.state.user
    # body = await request.json()
    body = None
    if error:
        error_detail = traceback.format_exc()

    user_log = dict(
        client=request.state.ip,
        name=user.name if user and user.name else None,
        email=user.email if user and user.email else None,
        address=user.address if user and user.address else None
    )

    log_dict = dict(
        url=request.url.hostname + request.url.path,
        method=str(request.method),
        statusCode=status_code,
        errorDetail=error_detail,
        client=user_log,
        processedTime=str(round(t * 1000, 5)) + "ms",
        datetimeKST=D.timestamp(),
    )


    if body:
        log_dict["body"] = body

    if error:
        logger.error(json.dumps(log_dict))
        # print(log_dict)
    else:
        logger.info(json.dumps(log_dict))