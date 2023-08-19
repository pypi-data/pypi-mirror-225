import contextlib
import threading
from typing import Generator

from anyio.abc import BlockingPortal
from anyio.from_thread import start_blocking_portal

from arraylake_client.log_util import get_logger

logger = get_logger(__name__)


BlockingPortalGenerator = Generator[BlockingPortal, None, None]

ANYIO_BACKEND = "asyncio"
ANYIO_BACKEND_OPTS = {"use_uvloop": True}


class CachedBlockingPortal:
    """
    Wrapper class to manage AnyIO blocking portal for use in synchronous contexts

    This class manages a single BlockingPortal and context. It keeps track of references to the
    BlockingPortal and only cleans up the portal once all references have exited the context
    manager provided by ``CachedBlockingPortal.acquire()``.
    """

    def __init__(self):
        self.ref_count = 0

        self._lock = threading.Lock()
        self._blocking_portal = None
        self._blocking_portal_context = None

    @contextlib.contextmanager
    def acquire(self) -> BlockingPortalGenerator:
        """
        Return a context manager that yields a blocking portal. Once all references have exited the
        context, close the portal.
        """
        with self._lock:
            logger.debug("entering CachedBlockingPortal.acquire", ref_count=self.ref_count)
            self.ref_count += 1
            if self.ref_count == 1:
                logger.debug("entering CachedBlockingPortal.acquire, starting portal")
                self._blocking_portal_context = start_blocking_portal(backend=ANYIO_BACKEND, backend_options=ANYIO_BACKEND_OPTS)
                self._blocking_portal = self._blocking_portal_context.__enter__()
        try:
            yield self._blocking_portal
        finally:
            with self._lock:
                self.ref_count -= 1
                logger.debug("exiting CachedBlockingPortal.acquire", ref_count=self.ref_count)
                if self.ref_count == 0:
                    logger.debug("exiting CachedBlockingPortal.acquire, exiting portal")
                    self._blocking_portal = None
                    self._blocking_portal_context.__exit__(None, None, None)
                    self._blocking_portal_context = None


#  Global portal - this should be used as the interface to the Blocking Portal throughout the client
# code base. In general, we should not need to instantiate the `CachedBlockingPortal` class elsewhere.
# Similarly, we should not need to call `start_blocking_portal` elsewhere.
cached_portal = CachedBlockingPortal()
