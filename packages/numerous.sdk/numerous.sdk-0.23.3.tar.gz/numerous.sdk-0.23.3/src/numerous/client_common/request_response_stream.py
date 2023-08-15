from time import sleep
from typing import Any, Callable, Generator, Iterable


class RequestResponseStream:
    # TODO: Implement async methods
    def __init__(
        self, stream_endpoint: Callable[[Iterable], Generator], check_delay: float = 0.1
    ):
        self._check_delay = check_delay

        self._request: Any = None
        self._response_iterator = stream_endpoint(self)

    def send(self, request):
        while self._request is not None:
            sleep(self._check_delay)
        self._request = request
        return next(self._response_iterator)

    def close(self):
        while self._request is not None:
            sleep(self._check_delay)
        self._request = StopIteration()

    def __iter__(self):
        return self

    def __next__(self):
        while self._request is None:
            sleep(self._check_delay)

        if type(self._request) is StopIteration:
            self._request = None
            raise StopIteration()

        request = self._request
        self._request = None
        return request

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # noqa: F841
        self.close()
