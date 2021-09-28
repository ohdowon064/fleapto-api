from os import environ



EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/auth)"
EXCEPT_API = {
    ("/api/product", "GET") : True,
    # ("/init", "DELETE") : True
}