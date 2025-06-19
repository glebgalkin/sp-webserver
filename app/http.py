class Request:
    def __init__(self, request_type: str, path: str, headers: dict, body: bytes = None):
        self.request_type = request_type
        self.path = path
        self.headers = headers
        self.body = body

class Response:
    def __init__(self, status: str, headers: dict, body = None):
        self.status = status
        self.headers = headers
        self.body = body
