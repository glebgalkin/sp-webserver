from app.http import Request
from app.router import Router


class SocketHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.request = None
        self.response = None

    def __enter__(self):
        print('Initializing client socket connection')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Closing client socket connection')
        self.client_socket.close()

    def handle_request(self):
        self.__parse_request()
        self.__route_request()
        self.__send_response()


    def __parse_request(self):
        data = self.client_socket.recv(1024).decode('utf-8')
        if not data:
            pass
        lines = data.split('\r\n')
        raw_title, raw_headers = lines[0], lines[1:]
        request_type, path, _ = raw_title.split(' ')
        headers = self.__parse_headers(raw_headers)
        self.request = Request(request_type, path, headers)

    def __route_request(self):
        router = Router(self.request)
        self.response = router.handle_endpoint()


    def __parse_headers(self, raw_headers: str) -> dict:
        headers = {}
        for line in raw_headers:
            if line:
                segments = line.split(' ')
                headers[segments[0][:-1]] = segments[1]
        return headers

    def __send_response(self):
        response_raw = [f'{self.response.status}\r\n']
        for key, val in self.response.headers.items():
            response_raw.append(f'{key}: {val}\r\n')
        response_raw.append(f'\r\n{self.response.body}')

        response_str = ''.join(response_raw)
        self.client_socket.send(response_str.encode('utf-8'))