from app.http import Response

class Router:
    def __init__(self, request):
        self.request = request

    def handle_endpoint(self) -> Response:
        if self.request.path.startswith('/encode'):
            return self.__handle_encode()
        elif self.request.path.startswith('/user-agent'):
            return self.__handle_user_agent()
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

    @staticmethod
    def __get_404():
        return Response('HTTP/1.1 404 Not Found')