
class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405

class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str
    ex: Exception

    def __init__(
            self,
            *,
            status_code: int = StatusCode.HTTP_500,
            code: str = "000000",
            msg: str = None,
            detail: str = None,
            ex: Exception = None
    ):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.detail = detail
        self.ex = ex
        super().__init__(ex)


class NotAuthorized(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg="로그인이 필요한 서비스입니다.",
            detail="Authorization Required",
            code=f"{StatusCode.HTTP_401}{'1'.zfill(4)}",
            ex=ex,
        )


class TokenExpiredEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg="세션이 만료되어 로그아웃 되었습니다.",
            detail="Token Expired",
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            ex=ex,
        )


class TokenDecodeEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg="비정상적인 접근입니다.",
            detail="Token has been compromised.",
            code=f"{StatusCode.HTTP_400}{'2'.zfill(4)}",
            ex=ex,
        )

class NotFoundEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            msg="존재하지 않는 접근입니다.",
            detail="Not Found Exception",
            code=f"{StatusCode.HTTP_404}{'3'.zfill(4)}",
            ex=ex
        )

class CanNotDeleteProductEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg="삭제할 수 있는 권한이 없습니다.",
            detail="Can Not Delete Product",
            code=f"{StatusCode.HTTP_401}{'4'.zfill(4)}",
            ex=ex
        )

class FailToDeleteProductEx(APIException):
    def __init__(self, product_id: str, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            msg=f"서버에서 요청한 상품 {product_id}를 삭제하는데 실패했습니다.",
            detail="Fail To Delete Product",
            code=f"{StatusCode.HTTP_500}{'5'.zfill(4)}",
            ex=ex
        )

class AlreadyExistEmailEx(APIException):
    def __init__(self, email: str, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"{email}은 이미 존재하는 이메일입니다.",
            detail="Already Exist Email",
            code=f"{StatusCode.HTTP_400}{'6'.zfill(4)}",
            ex=ex
        )