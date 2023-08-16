import uuid
from typing import Any, Callable, Optional

import grpc
from grpc_interceptor import ClientCallDetails, ClientInterceptor


class ValidationInterceptor(ClientInterceptor):
    def __init__(
        self, token, token_callback: Callable[[], str], instance: Optional[str] = None
    ):
        self.token = token
        self.instance = str(uuid.uuid4()) if instance is None else instance
        self.token_callback = token_callback

    def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ):
        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            [("token", self.token_callback()), ("instance", str(self.instance))],
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )

        return method(request_or_iterator, new_details)
