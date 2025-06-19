from app.http import Response

from abc import ABC, abstractmethod

class ResponseConverter(ABC):
    @abstractmethod
    def convert(self, response: Response):
        pass


class ResponseConverterImpl(ResponseConverter):
    def convert(self, response: Response):
        pass
