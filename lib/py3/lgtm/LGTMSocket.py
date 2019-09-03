from types import TracebackType
from typing import Optional, Type

import errno
import logging
import os
import socket
import stat


class LGTMSocket(object):
    def __init__(self, path: str = "/mnt/ipc/lgtm.ipc"):
        self._path: str = path

    def __enter__(self) -> socket.socket:
        if (
            not os.path.exists(self._path)
            or os.stat(self._path).st_mode & stat.S_IFSOCK != stat.S_IFSOCK
        ):
            raise OSError(
                errno.EEXIST, f"Path {self._path} does not exist or is not a socket."
            )
        self.s: socket.socket = socket.socket(socket.AF_UNIX)
        self.s.connect(self._path)
        return self.s

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        try:
            self.s.close()
        except Exception:
            logging.warning("Failed to close socket %r.", self._path, exc_info=True)
