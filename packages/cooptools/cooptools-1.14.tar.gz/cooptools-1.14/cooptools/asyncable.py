import threading
import time
from typing import Callable

class Asyncable:
    def __init__(self,
                 loop_callback: Callable,
                 as_async: bool = False,
                 start_on_init: bool = False,
                 loop_timeout_ms: int = 100,
                 ):
        self._as_async = as_async
        self._start_thread_on_init = start_on_init
        self._async = as_async
        self._thread = None
        self._loop_timeout_ms = max(loop_timeout_ms, 10)
        self._callback = loop_callback

        # start thread on init
        if self._async and self._start_thread_on_init:
            self.start()

    def start(self):
        self._async = True
        self._thread = threading.Thread(target=self._async_loop, daemon=True)
        self._thread.start()

    def stop(self):
        if self._thread is not None:
            self._async = False
            self._thread.join()

    def _async_loop(self):
        while True:
            self._callback()
            time.sleep(self._loop_timeout_ms / 1000)