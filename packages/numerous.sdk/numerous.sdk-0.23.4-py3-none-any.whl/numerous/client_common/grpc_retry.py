import logging
from functools import wraps
from time import sleep

import grpc

log = logging.getLogger(__name__)


def _grpc_backoff(
    start_delay: float, attempt_number: int, max_attempts: int, rpc_error: grpc.RpcError
):
    if rpc_error.code() in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.INTERNAL):
        if attempt_number == max_attempts:
            log.warning("Exceeded command retry attempts")
            raise rpc_error
        timeout = start_delay * 2**attempt_number
        log.warning(
            f"Got error: {rpc_error}, wait for {timeout} seconds and retry the command"
        )
        sleep(timeout)
    else:
        raise rpc_error


def grpc_retry_stream(max_attempts: int = 5, start_delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for attempt_number in range(1, max_attempts + 1):
                try:
                    yield from func(self, *args, **kwargs)
                    return
                except grpc.RpcError as e:
                    _grpc_backoff(start_delay, attempt_number, max_attempts, e)

        return wrapper

    return decorator


def grpc_retry_unary(max_attempts: int = 5, start_delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for attempt_number in range(1, max_attempts + 1):
                try:
                    return func(self, *args, **kwargs)
                except grpc.RpcError as e:
                    _grpc_backoff(start_delay, attempt_number, max_attempts, e)

        return wrapper

    return decorator


grpc_retry = grpc_retry_unary  # TODO: deprecate this for grpc_retry_unary
