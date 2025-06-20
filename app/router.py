from app.http import Response
from app.file_util import get_file, get_content_type, get_file_size_bytes


class Router:
    def __init__(self, request):
        self.request = request

    def handle_endpoint(self) -> Response:
        if self.request.path.startswith('/encode'):
            return self.__handle_encode()
        elif self.request.path.startswith('/user-agent'):
            return self.__handle_user_agent()
        elif self.request.path.startswith('/file'):
            return self.__handle_file()
        else:
            return self.__get_404()

    def __handle_encode(self) -> Response:
        path = self.request.path
        body = ''.join(path.split('/')[2:])

        size = str(len(body.encode('utf-8')))
        headers = {
            'Content-Type': 'text/plain',
            'Content-Length': size
        }
        return Response('HTTP/1.1 200 OK', headers, body)

    def __handle_user_agent(self) -> Response:
        body = self.request.headers['User-Agent']
        size = str(len(body.encode('utf-8')))
        headers = {
            'Content-Type': 'text/plain',
            'Content-Length': size
        }
        return Response('HTTP/1.1 200 OK', headers, body)

    def __handle_file(self) -> Response:
        filename = self.request.path.split('/')[2]
        filepath = get_file(filename)
        if not filepath:
            return self.__get_404()
        headers = {
            'Content-Type': get_content_type(filename),
            'Content-Length': get_file_size_bytes(filepath)
        }
        return Response('HTTP/1.1 200 OK', headers, body=filepath)

    @staticmethod
    def __get_404():
        return Response('HTTP/1.1 404 Not Found')
