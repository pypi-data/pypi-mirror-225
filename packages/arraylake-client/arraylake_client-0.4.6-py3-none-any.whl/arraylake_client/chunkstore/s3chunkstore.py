import importlib
import logging
from collections import deque
from functools import lru_cache
from typing import Callable, Deque, Mapping, Optional
from urllib.parse import urlparse

import numpy as np
from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session

from arraylake_client.chunkstore.abc import Chunkstore
from arraylake_client.config import config
from arraylake_client.types import ChunkHash, ReferenceData

logger = logging.getLogger(__name__)


class HashValidationError(AssertionError):
    pass


def tokenize(data: bytes, *, hasher: Callable) -> str:
    hash_obj = hasher(data)
    return hash_obj.hexdigest()


@lru_cache(maxsize=None)
def get_hasher(method):
    try:
        mod_name, func_name = method.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        return getattr(mod, func_name)
    except (ImportError, AttributeError):
        raise ValueError(f"invalid hash method {method}")


class S3Chunkstore(Chunkstore):
    """S3Chunkstore interface"""

    uri: str
    client_kws: Mapping[str, str]
    _OPEN: bool
    _session_client: Optional[AioBaseClient]
    _known_key_cache: Optional[Deque]

    def __init__(self, uri: str, **client_kws):
        """
        Args:
            uri: Address of chunk store service. For example: ``s3://chunkstore``.
            client_kws: Additional keyword arguments to pass to
                ``aiobotocore.session.AIOSession.session.create_client``, by default None.
        """
        if not uri.startswith("s3://"):
            raise ValueError("Chunkstore uri must be a s3 path")
        self.uri = uri
        self.client_kws = client_kws
        self._set_props()
        self._client_context = None
        self._session_client = None
        self._OPEN = False

        self._setup_chunk_key_cache()

    def _set_props(self):
        parsed_uri = urlparse(self.uri)
        self._service_name = parsed_uri.scheme
        self._bucket = parsed_uri.netloc
        self._path = parsed_uri.path.lstrip("/")

    def __getstate__(self):
        return self.uri, self.client_kws

    def __setstate__(self, state):
        self.uri, self.client_kws = state
        self._set_props()
        self._OPEN = False
        self._setup_chunk_key_cache()

    async def __aenter__(self):
        self._client_context = get_session().create_client(self._service_name, **self.client_kws)
        self._session_client = await self._client_context.__aenter__()
        self._OPEN = True
        return self

    async def __aexit__(self, *args):
        await self._client_context.__aexit__(*args)
        self._session_client = None
        self._OPEN = False

    def _setup_chunk_key_cache(self):
        self._known_key_cache = deque(maxlen=5000)  # tunable

    def __repr__(self):
        status = "OPEN" if self._OPEN else "CLOSED"
        return f"<arraylake_client.s3_chunkstore.S3Chunkstore uri='{self.uri}' status={status}>"

    async def ping(self):
        """Check if the chunk store bucket exists."""
        # Should raise an exception if the bucket does not exist
        await self._session_client.head_bucket(Bucket=self._bucket)

    async def add_chunk(self, data: bytes, *, hash_method: str = None) -> ReferenceData:
        if isinstance(data, np.ndarray):
            # We land here if the data are not compressed by a codec. This happens for 0d arrays automatically.
            data = data.tobytes()

        if hash_method is None:
            hash_method = config.get("chunkstore.hash_method", "hashlib.sha256")

        hasher = get_hasher(hash_method)

        token = tokenize(data, hasher=hasher)
        key = f"{self._path}{token}"

        uri = f"{self._service_name}://{self._bucket}/{key}"
        length = len(data)
        chunk_ref = ReferenceData(uri=uri, offset=0, length=length, hash=ChunkHash(method=hash_method, token=token))

        if token not in self._known_key_cache:
            resp = await self._session_client.put_object(Bucket=self._bucket, Key=key, Body=data)
            self._known_key_cache.append(token)
            logger.debug(resp)

        return chunk_ref

    async def get_chunk(self, chunk_ref: ReferenceData, *, validate: bool = False) -> bytes:
        logger.debug("get_chunk %s", chunk_ref)

        parsed_uri = urlparse(chunk_ref.uri)
        key = parsed_uri.path.strip("/")
        bucket = parsed_uri.netloc

        start_byte = chunk_ref.offset
        # stop_byte is inclusive, in contrast to python indexing conventions
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Range
        stop_byte = chunk_ref.offset + chunk_ref.length - 1
        byte_range = f"bytes={start_byte}-{stop_byte}"
        response = await self._session_client.get_object(Bucket=bucket, Key=key, Range=byte_range)
        logger.debug(response)
        async with response["Body"] as stream:
            data = await stream.read()

        if validate:
            hasher = get_hasher(chunk_ref.hash["method"])
            h = tokenize(data, hasher=hasher)
            if h != chunk_ref.hash["token"]:
                raise HashValidationError(f"hashes did not match for key: {key}")

        return data
