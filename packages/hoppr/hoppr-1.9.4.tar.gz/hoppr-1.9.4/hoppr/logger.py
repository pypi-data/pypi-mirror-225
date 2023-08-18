"""
A logger that gets dumped to stdout when closed
"""
from __future__ import annotations

import functools
import inspect
import itertools
import logging

from logging import FileHandler, Formatter, Logger
from logging.handlers import MemoryHandler
from threading import _RLock as RLock
from threading import get_ident
from typing import Callable


def locked(func: Callable) -> Callable:
    """
    Acquire logfile lock, run the wrapped function, then release the lock
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.lock:
            self.lock.acquire()

        func(self, *args, **kwargs)

        if self.lock:
            self.lock.release()

    return wrapper


class HopprLogger(Logger):
    """
    Logger that buffers log records in memory until flushed
    """

    id_iter = itertools.count()

    def __init__(  # pylint: disable=too-many-arguments
        self,
        file_name: str,
        lock: RLock | None = None,
        log_name: str | None = None,
        log_level: int = logging.INFO,
        flush_immed: bool = False,
    ) -> None:
        self.file_name = file_name
        self.flush_immed = flush_immed
        self.instance_id = next(self.id_iter)
        self.lock = lock

        caller = inspect.stack()[1].function

        caller_cls = inspect.stack()[1].frame.f_locals.get("self", None)
        if caller_cls is not None:
            caller = type(caller_cls).__name__

        log_name = log_name or f"{caller}-{get_ident()}-{self.instance_id}"

        super().__init__(name=log_name, level=log_level)

        formatter = Formatter(
            fmt="[$asctime] - [${caller}] - [$levelname] - $message",
            style="$",
            defaults={"caller": caller},
        )

        file_handler = FileHandler(file_name)
        file_handler.setFormatter(formatter)

        self.log_handler = MemoryHandler(10000, flushLevel=logging.CRITICAL, target=file_handler)

        self.addHandler(self.log_handler)

    def is_verbose(self) -> bool:
        """
        Check whether running with `--debug`/`--verbose` flag
        """
        return self.level == logging.DEBUG

    @locked
    def flush(self) -> None:
        """
        Flush all handlers for this logger
        """
        for handler in self.handlers:
            handler.flush()

    @locked
    def close(self) -> None:
        """
        Close (and flush) all handlers for this logger
        """
        for handler in self.handlers:
            handler.close()

    def clear_targets(self) -> None:
        """
        Makes the target for all Memory Handlers in this logger None

        Thus when these handlers are flushed, nothing will go to standard output
        """
        for handler in self.handlers:
            if isinstance(handler, MemoryHandler):
                handler.setTarget(None)

    def log(self, level: int, msg: str, *args, indent_level: int = 0, **kwargs) -> None:  # type: ignore[override]
        """
        Wrapper function for logging messages
        """
        indent_string = " " * 4 * indent_level
        msg = f"{indent_string}{msg}"

        filename, lno, func, sinfo = self.findCaller(stack_info=False, stacklevel=1)
        record = self.makeRecord(
            self.name, level, filename, lno, msg, args, exc_info=None, func=func, extra=None, sinfo=sinfo
        )

        if level >= self.level:
            self.log_handler.buffer.append(record)

        if self.flush_immed:
            self.flush()

    def debug(self, msg: str, *args, indent_level: int = 0, **kwargs) -> None:  # type: ignore[override]
        """
        Wrapper function for debug messages
        """
        self.log(logging.DEBUG, msg, *args, indent_level=indent_level, **kwargs)

    def info(self, msg: str, *args, indent_level: int = 0, **kwargs) -> None:  # type: ignore[override]
        """
        Wrapper function for info messages
        """
        self.log(logging.INFO, msg, *args, indent_level=indent_level, **kwargs)

    def warning(self, msg: str, *args, indent_level: int = 0, **kwargs) -> None:  # type: ignore[override]
        """
        Wrapper function for warn messages
        """
        self.log(logging.WARNING, msg, *args, indent_level=indent_level, **kwargs)

    def error(self, msg: str, *args, indent_level: int = 0, **kwargs) -> None:  # type: ignore[override]
        """
        Wrapper function for error messages
        """
        self.log(logging.ERROR, msg, *args, indent_level=indent_level, **kwargs)

    def fatal(self, msg: str, *args, indent_level: int = 0, **kwargs) -> None:  # type: ignore[override]
        """
        Wrapper function for fatal messages
        """
        self.log(logging.FATAL, msg, *args, indent_level=indent_level, **kwargs)

    def critical(self, msg: str, *args, indent_level: int = 0, **kwargs) -> None:  # type: ignore[override]
        """
        Wrapper function for critical messages
        """
        self.log(logging.CRITICAL, msg, *args, indent_level=indent_level, **kwargs)
