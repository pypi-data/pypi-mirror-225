from arraylake_client.chunkstore.abc import Chunkstore
from arraylake_client.chunkstore.s3chunkstore import S3Chunkstore


def chunkstore(chunkstore_uri: str, **kwargs) -> Chunkstore:
    """Initialize a Chunkstore

    Args:
        chunkstore_uri: URI to chunkstore.
        kwargs: Additional keyword arguments to pass to the chunkstore constructor.

    Returns:
        chunkstore:
    """
    if chunkstore_uri and chunkstore_uri.startswith("s3://"):
        return S3Chunkstore(chunkstore_uri, **kwargs)
    else:
        raise ValueError(f"Cannot parse chunkstore uri {chunkstore_uri}, supported prefixes are: ['s3://']")
