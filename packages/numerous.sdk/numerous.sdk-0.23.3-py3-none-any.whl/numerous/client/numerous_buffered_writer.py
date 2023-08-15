import sys
import threading
from datetime import datetime
from queue import Queue
from time import sleep, time
from typing import Any, Callable, Generator, Optional, Protocol

from numerous.client import config

from .common import log, trace

FLOAT_SIZE = sys.getsizeof(float(0))

WRITE_MAX_ATTEMPTS = 5
WRITE_ERROR_ATTEMPT_RESET_SECONDS = 10
WRITE_BACKOFF_START_DELAY = 1


class WriteMethodProtocol(Protocol):
    def __call__(
        self,
        data_generator: Generator[dict[str, float], None, None],
        scenario: Optional[str] = None,
        clear: bool = False,
        must_flush: Optional[Callable[[int, int], bool]] = None,
        execution: Optional[str] = None,
        last_item_index: int = 0,
    ) -> None:
        pass


class NumerousBufferedWriter:
    def __init__(
        self,
        write_method: WriteMethodProtocol,
        writer_closed_method,
        scenario: str,
        buffer_size: int = 24 * 7,
        logger: Optional[Any] = None,
        trace: bool = False,
    ):
        self.scenario = scenario
        self._tags = None
        self.ix = 0
        self._write_method = write_method
        self._writer_closed = writer_closed_method
        self._buffer = None
        self.buffer_size = buffer_size
        self.write_queue: Queue[dict[str, float]] = Queue()
        self.closed = False

        self.logger = logger  # for trace decorator
        self.trace = trace  # for trace decorator

        self.last_flush = time()
        self.max_elapse_flush = 600
        self.min_elapse_flush = 1
        self.force_flush = False
        self.buffer_number_size = 1e6
        self._last_item_index = 0
        self._restore_row: Optional[dict[str, float]] = None
        self._last_row: Optional[dict[str, float]] = None
        self._writer_thread = threading.Thread(
            target=self._writer_thread_func, daemon=True
        )
        self._writer_thread.start()

    def _write_generator(self) -> Generator[dict[str, float], None, None]:
        while True:
            if row := self._restore_row:
                self._restore_row = None
            else:
                row = self.write_queue.get()
                if row == "STOP":
                    return
            self._last_row = row
            self._last_item_index += 1
            yield row

    def _writer_thread_func(self) -> None:
        last_error_time: Optional[float] = None
        failed_attempts: int = 0

        while failed_attempts < WRITE_MAX_ATTEMPTS:
            try:
                log.debug("Starting writer, attempt=%s", failed_attempts)
                self._write_method(
                    self._write_generator(),
                    must_flush=self._must_flush,
                    last_item_index=self._last_item_index,
                )
                return
            except Exception:
                elapsed_since_last_error = (
                    time() - last_error_time if last_error_time else 0.0
                )
                if elapsed_since_last_error > WRITE_ERROR_ATTEMPT_RESET_SECONDS:
                    failed_attempts = 0

                log.exception("An error occured writing data, retrying...")
                back_off_time = WRITE_BACKOFF_START_DELAY * 2**failed_attempts
                self._restore_row = self._last_row
                failed_attempts += 1
                sleep(back_off_time)
        log.error("Shutting down writer thread due to many attempts")

    def _must_flush(self, n_rows, rows_size):
        estimated_size = n_rows * rows_size * FLOAT_SIZE
        elapsed_since_last_flush = time() - self.last_flush
        if self.force_flush:
            self.force_flush = False
            self.last_flush = time()
            return True
        elif (
            n_rows > self.buffer_size
            and elapsed_since_last_flush > self.min_elapse_flush
        ) or estimated_size * 1.1 > config.GRPC_MAX_MESSAGE_SIZE:
            self.last_flush = time()
            return True
        elif elapsed_since_last_flush > self.max_elapse_flush:
            self.last_flush = time()
            return True
        return False

    def _init_buffer(self):
        self._buffer_count = 0
        # self._buffer = {t: [] for t in self._tags}
        self._buffer_timestamp = []

    @trace
    def write_row(self, data):
        if "_index" not in data:
            data["_index"] = self.ix
            self.ix += 1

        if isinstance(data["_index"], datetime):
            data["_index"] = data["_index"].timestamp()
        if self.closed:
            raise ValueError("Queue is closed!")
        self.write_queue.put(data)
        return data["_index"]

    @trace
    def flush(self):
        self.force_flush = True
        # self._write_method(self._buffer, self.scenario)
        self._init_buffer()

    @trace
    def close(self):
        if not self.closed:
            self.flush()
            self.write_queue.put("STOP")
            self._writer_thread.join()
            self._writer_closed(self.scenario)

        self.closed = True
