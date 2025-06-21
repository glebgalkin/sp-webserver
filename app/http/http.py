from enum import Enum


class Request:
    def __init__(self, request_type: str, path: str, headers: dict, body: bytes = None):
        self.request_type = request_type
        self.path = path
        self.headers = headers
        self.body = body


class Response:
    def __init__(self, status: str, headers: dict = None, body=None):
        self.status = status
        self.headers = headers
        self.body = body


def get_basic_headers(content_type: str, content_length: int) -> dict:
    return {
        'Content-Type': content_type,
        'Content-Length': str(content_length)
    }


class ResponseStatus(Enum):
    OK = 'HTTP/1.1 200 OK'
    NOT_FOUND = 'HTTP/1.1 404 Not Found'
    SERVICE_UNAVAILABLE = 'HTTP/1.1 503 Service Unavailable'
