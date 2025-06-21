from app.file_utils.file_util import get_file, get_content_type, get_file_size_bytes, save_file
from app.http.http import Response, get_basic_headers, ResponseStatus
from app.http.http_util import parse_filename
import gzip


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
        elif self.request.request_type == 'POST' and self.request.path.startswith('/upload'):
            return self.__handle_file_upload()
        elif self.request.request_type == 'POST' and self.request.path.startswith('/json'):
            return self.__handle_json()
        else:
            return self.__get_404()

    def __handle_encode(self) -> Response:
        path = self.request.path
        body = ''.join(path.split('/')[2:])

        size = len(body.encode('utf-8'))
        headers = get_basic_headers('text/plain', size)
        return Response(ResponseStatus.OK.value, headers, body)

    def __handle_user_agent(self) -> Response:
        body = self.request.headers['User-Agent']
        size = len(body.encode('utf-8'))
        headers = get_basic_headers('text/plain', size)
        return Response(ResponseStatus.OK.value, headers, body)

    def __handle_file(self) -> Response:
        filename = self.request.path.split('/')[2]
        filepath = get_file(filename)
        if not filepath:
            return self.__get_404()

        headers = get_basic_headers(get_content_type(filename), get_file_size_bytes(filepath))
        return Response(ResponseStatus.OK.value, headers, body=filepath)

    def __handle_file_upload(self) -> Response:
        filename = parse_filename(self.request.path)
        save_file(filename, self.request.body)
        return Router.__get_200()

    def __handle_json(self) -> Response:
        size = len(self.request.body)
        print('JSON Body size: ', size)
        if self.__is_supports_compression():
            body_compressed = gzip.compress(self.request.body)
            content_length = len(body_compressed)
            print('Compressed JSON size: ', content_length)
            headers = get_basic_headers('application/json', content_length)
            headers['Content-Encoding'] = 'gzip'

            return Response(ResponseStatus.OK.value, headers, body_compressed)

        else:
            headers = get_basic_headers('text/plain', size)
            return Response(ResponseStatus.OK.value, headers, self.request.body)


    def __is_supports_compression(self):
        return 'Accept-Encoding' in self.request.headers

    @staticmethod
    def __get_200():
        return Response(ResponseStatus.OK.value)

    @staticmethod
    def __get_404():
        return Response(ResponseStatus.NOT_FOUND.value)

    @staticmethod
    def __get_503():
        return Response(ResponseStatus.SERVICE_UNAVAILABLE.value)
