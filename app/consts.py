from os import environ

STAGE = environ.get("STAGE", "local")
ROOT_PATH = f"/{STAGE}" if STAGE and STAGE != "local" else ""

EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/auth)"