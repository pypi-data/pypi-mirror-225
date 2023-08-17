from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class ErrorCodeText:
    INVALID_DATA = "INVALID_DATA"
    ACCESS_DENIED = "ACCESS_DENIED"
    UNIQUE_CONSTRAINT = "UNIQUE_CONSTRAINT"

def get_error_response(error_code: str, errors: dict):
    return {"code": error_code, "errors": errors}

def get_message_response(message_code: str, messages: list):
    return {"code": message_code, "messages": messages}

class RequestMethodType:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

default_authentication_classes = [
    # BasicAuthentication,
    TokenAuthentication
]
default_permission_classes = (IsAuthenticated,)
