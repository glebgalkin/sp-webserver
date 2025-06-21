from socket import socket

from app.http import Request
from app.router import Router
from pathlib import Path


class SocketHandler:
    CHUNK_SIZE = 1024
    DEFAULT_ENCODING = 'utf-8'

    def __init__(self, client_socket: socket):
        self.client_socket = client_socket
        self.request = None
        self.response = None

    @staticmethod
    def __parse_headers(raw_headers: list[str]) -> dict:
        headers = {}
        for line in raw_headers:
            if line:
                key, val = line.split(': ', 1)
                headers[key] = val.strip()
        return headers

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

        # Step 1: Read until we hit end of headers
        data = b''
        while b'\r\n\r\n' not in data:
            data += self.client_socket.recv(1024)

        # Step 2: Split what we've got into headers + partial body
        header_data_bytes, body_data = data.split(b'\r\n\r\n', 1)

        # Step 3: Parse headers to know how much body to expect
        header_data = header_data_bytes.decode(SocketHandler.DEFAULT_ENCODING)
        title_raw, headers_raw = header_data.split('\r\n', 1)
        request_type, path, _ = title_raw.split(' ')

        headers = dict(header_line.split(':', 1) for header_line in headers_raw.split('\r\n'))
        content_length = int(headers.get('Content-Length', 0))

        while len(body_data) < content_length:
            body_data += self.client_socket.recv(1024)

        self.request = Request(request_type, path, headers, body_data)

    def __route_request(self):
        router = Router(self.request)
        self.response = router.handle_endpoint()

    def __send_response(self):
        response_raw = [f'{self.response.status}\r\n']
        if self.response.headers:
            for key, val in self.response.headers.items():
                response_raw.append(f'{key}: {val}\r\n')

        response_raw.append('\r\n')

        if self.response.body:
            if isinstance(self.response.body, str):
                response_raw.append(self.response.body)
                response_str = ''.join(response_raw)
                self.client_socket.send(response_str.encode(SocketHandler.DEFAULT_ENCODING))
            elif isinstance(self.response.body, Path):
                response_str = ''.join(response_raw)
                self.client_socket.send(response_str.encode(SocketHandler.DEFAULT_ENCODING))
                with open(self.response.body, 'rb') as f:
                    while chunk := f.read(SocketHandler.CHUNK_SIZE):
                        self.client_socket.sendall(chunk)
        else:
            self.client_socket.send(''.join(response_raw).encode(SocketHandler.DEFAULT_ENCODING))