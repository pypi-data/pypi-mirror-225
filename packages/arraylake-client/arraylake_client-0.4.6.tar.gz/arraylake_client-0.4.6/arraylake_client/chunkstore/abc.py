from __future__ import annotations

from abc import ABC, abstractmethod

from arraylake_client.types import ReferenceData


class Chunkstore(ABC):  # pragma: no cover
    @abstractmethod
    async def __aenter__(self):
        """Enter async context"""
        ...

    @abstractmethod
    async def __aexit__(self, *args, **kwargs):
        """Exit async context"""
        ...

    @abstractmethod
    async def ping(self):
        """Ping the chunkstore to check connectivity"""
        ...

    @abstractmethod
    async def add_chunk(self, data: bytes, *, hash_method: str = None) -> ReferenceData:
        """Add a chunk to the chunkstore

        Args:
            data: Bytestring to add to the chunkstore
            hash_method: Key generation method. May be any hash function that returns an object with the
                ``hexdigest()`` method. Valid examples are ``{'hashlib.sha256', 'hashlib.md5', 'xxhash.xxh128'}``.
                 Default can be set in the ``chunkstore.hash_method`` config key.

        Returns:
            chunk_ref: Dict of reference metadata about written chunk
        """
        ...

    @abstractmethod
    async def get_chunk(self, chunk_ref: ReferenceData, *, validate: bool = False) -> bytes:
        """Get a chunk from the chunkstore

        Args:
            chunk_ref: Dict of reference metadata about written chunk
            validate: If True, then validate the chunks data with its reference hash.

        Returns:
            data: Chunk byte string
        """
        ...
