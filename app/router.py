from http.client import responses

from app.http import Response


class Router:
    def __init__(self, request):
        self.request = request

    def handle_endpoint(self) -> Response:
        if self.request.path.startswith('/encode'):
            return self.__handle_encode()
        elif self.request.path.startswith('/user-agent'):
            return self.__handle_user_agent()


    def __handle_encode(self) -> Response:
        path = self.request.path
        body = ''.join(path.split('/')[2:])

        size = str(len(body.encode('utf-8')))
        headers = {
            'Content-Type': 'text/plain',
            'Content-Length': size
        }
        return Response('HTTP/1.1 200 OK', headers, body)
        # return Response('200 OK', headers, body.encode('utf-8'))

    def __handle_user_agent(self) -> Response:
        body = self.request.headers['User-Agent']
        size = str(len(body.encode('utf-8')))
        headers = {
            'Content-Type': 'text/plain',
            'Content-Length': size
        }
        return Response('HTTP/1.1 200 OK', headers, body)


'''
Content-Type	What type of data is in the body (e.g. text/html, application/json, text/plain)
Content-Length	Size of the response body in bytes
Date	Current date/time of the response
Server	(Optional) Info about the server software
Connection	(Optional) e.g. keep-alive or close
Access-Control-Allow-Origin	(for APIs) allows cross-origin requests
Cache-Control	Controls caching (e.g. no-cache, max-age)
Set-Cookie	If you want to set cookies in the client
'''