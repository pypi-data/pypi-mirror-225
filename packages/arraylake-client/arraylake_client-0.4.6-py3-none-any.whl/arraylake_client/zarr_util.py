import json
import re

meta_root = "meta/root/"
data_root = "data/root/"

# https://zarr-specs.readthedocs.io/en/latest/core/v3.0.html#entry-point-metadata
ENTRY_POINT_METADATA = json.dumps(
    {
        "zarr_format": "https://purl.org/zarr/spec/core/3.0",
        "metadata_encoding": "https://purl.org/zarr/spec/core/3.0",
        "metadata_key_suffix": ".json",
        "extensions": [],
    }
).encode()


def is_chunk_key(key):
    return key.startswith("data/")


def is_meta_key(key):
    return key.startswith("meta/") or key == "zarr.json"


def is_v2_chunk_key(key):
    """is key a valid v2 key

    examples:
      - "foo/bar/spam/1.2.3.4"
      - "foo/bar/0.0"
      - "foo/0"
    """
    segments = key.split("/")
    if segments:
        last_segment = segments[-1]
        return re.match(r"^(\d+\.)*\d+$", last_segment) is not None
