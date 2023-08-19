import json
from enum import Enum
from typing import Any, Dict, List, Tuple, Union
from urllib.parse import urlparse

from pydantic import BaseModel

from arraylake_client.config import config
from arraylake_client.log_util import get_logger
from arraylake_client.types import Path, ReferenceData
from arraylake_client.zarr_util import (
    data_root,
    is_chunk_key,
    is_meta_key,
    is_v2_chunk_key,
    meta_root,
)

logger = get_logger(__name__)


class FileType(Enum):
    hdf5 = 1
    netcdf3 = 2


# type definitions
ChunkRefT = List[Union[str, int]]
MetaDictT = Dict[str, Any]
ReferenceStoreT = Dict[Path, Union[MetaDictT, ChunkRefT]]


# pydantic models
class ChunkGrid(BaseModel):
    chunk_shape: List[int]
    separator: str = "/"
    type: str = "regular"


class Codec(BaseModel):
    codec: str
    configuration: dict


class V3ArrayMeta(BaseModel):
    attributes: dict = {}
    chunk_grid: ChunkGrid
    chunk_memory_layout: str
    compressor: Codec = None  # TODO: this will become codecs: list[]
    data_type: str
    extensions: List = []
    fill_value: Any
    shape: List[int]


class V3GroupMeta(BaseModel):
    attributes: dict = {}


def guess_file_type(fp) -> FileType:
    magic = fp.read(4)
    fp.seek(0)
    if magic[:3] == b"CDF":
        return FileType.netcdf3
    elif magic == b"\x89HDF":
        return FileType.hdf5
    else:
        raise ValueError(f"Unknown file type - magic {magic}")


def make_v3_array(zattrs: Dict[str, Any], zarray: Dict[str, Any]) -> V3ArrayMeta:
    chunk_grid = ChunkGrid(
        chunk_shape=zarray["chunks"],
    )

    v2_compressor_config = zarray["compressor"]
    if v2_compressor_config is not None:
        v2_compressor_id = v2_compressor_config.pop("id", None)
        compressor = Codec(
            codec=f"https://purl.org/zarr/spec/codec/{v2_compressor_id}/1.0",
            configuration=v2_compressor_config,
        )
    else:
        compressor = None

    if "filters" in zarray:
        zattrs["filters"] = zarray.pop("filters")

    array = V3ArrayMeta(
        attributes=zattrs,
        chunk_grid=chunk_grid,
        chunk_memory_layout=zarray["order"],
        compressor=compressor,
        data_type=zarray["dtype"],
        fill_value=zarray["fill_value"],
        shape=zarray["shape"],
    )
    return array


def _maybe_load_json(obj: Union[MetaDictT, bytes, str]) -> MetaDictT:
    """load json to dict if obj is string or bytes"""
    if isinstance(obj, (str, bytes)):
        return json.loads(obj)
    return obj


def make_v3_store(store_v2: Dict[str, Any]) -> ReferenceStoreT:
    """
    Given a mapping with Zarr V2 keys and references, return an equivalent Zarr V3 mapping

    Parameters
    ----------
    store_v2 : dict
        Mapping with Zarr V2 keys, Zarr V2 metadata objects, and chunk references (3 element list)

    Returns
    -------
    new_store : dict
        New store with Zarr V3 keys and metadata objects.
    """
    new_store: ReferenceStoreT = {}
    for key, doc in store_v2.items():
        # root group
        # TODO: handle case where there is no root group in store or the root of store_v2 is not /
        if key == ".zgroup":
            doc = _maybe_load_json(doc)
            new_key = "meta/root.group.json"
            attrs = _maybe_load_json(store_v2.get(".zattrs", {}))
            obj = V3GroupMeta(attributes=attrs).dict()
            new_store[new_key] = obj
        # arbitrary groups/arrays
        elif key.endswith(".zarray"):
            doc = _maybe_load_json(doc)
            new_key = meta_root + key.replace("/.zarray", ".array.json")
            attrs_key = key.replace(".zarray", ".zattrs")
            attrs = _maybe_load_json(store_v2.get(attrs_key, {}))
            obj = make_v3_array(attrs, doc).dict()
            new_store[new_key] = obj
        elif key.endswith(".zgroup"):
            new_key = meta_root + key.replace("/.zgroup", ".group.json")
            attrs_key = key.replace(".zgroup", ".zattrs")
            attrs = _maybe_load_json(store_v2.get(attrs_key, {}))
            obj = V3GroupMeta(attributes=attrs).dict()
            new_store[new_key] = obj
        # skip .zattrs because we already captured them in the group/array steps
        elif key.endswith(".zattrs"):
            continue
        # skip the .zmetadata (we don't need it)
        elif key.endswith(".zmetadata"):
            continue
        # chunks
        elif is_v2_chunk_key(key):
            var, chunk = key.rsplit("/", maxsplit=1)
            new_key = f"{data_root}{var}/c" + chunk.replace(".", "/")
            new_store[new_key] = doc

        else:
            logger.warning(f"skipping unrecognized key: {key}")

    return new_store


def scan_netcdf(url: str, **kwargs) -> ReferenceStoreT:
    """
    Scan a NetCDF file in S3 and return Kerchunk-style references for all keys.

    Parameters
    ----------
    url : str
        URL to NetCDF file. Must start with `s3://` and may include sub directories (e.g. `s3://foo/bar`)

    Returns
    -------
    refs : dict
        Kerchunk-style references for all keys in NetCDF file
    """
    import s3fs

    if not url.startswith("s3:"):
        raise NotImplementedError(f"Only s3 urls are supported. Got {url}")

    if "storage_options" in kwargs:
        raise ValueError("Storage options are configured automatically by Arraylake. Do not pass `storage_options`.")
    if "inline_threshold" in kwargs:
        raise ValueError("Arraylake does not support inlining of data. Do not pass `inline_threshold`.")

    # TODO: replace this workaround with more generic handling of S3 options
    storage_options = {}
    endpoint_url = config.get("s3.endpoint_url", None)
    if endpoint_url:
        storage_options = {"client_kwargs": {"endpoint_url": endpoint_url}}
    s3 = s3fs.S3FileSystem(**storage_options)

    with s3.open(url) as fp:
        file_type = guess_file_type(fp)
        if file_type == FileType.hdf5:
            from kerchunk.hdf import SingleHdf5ToZarr

            scan = SingleHdf5ToZarr(fp, url, inline_threshold=0, spec=0, **kwargs)
        elif file_type == FileType.netcdf3:
            from kerchunk.netCDF3 import NetCDF3ToZarr

            # here the kerchunk API is very inconsistent
            # while SingleHdf5ToZarr can take a file-like object, NetCDF3ToZarr requires a url, plus the storage options
            scan = NetCDF3ToZarr(url, storage_options=storage_options, inline_threshold=0, **kwargs)
        refs = scan.translate()

    if "refs" in refs:
        # another kerchunk API inconsistency
        # outputs from NetCDF3ToZarr are nested in a "refs" key for some reason
        refs = refs["refs"]

    return refs


def scan_zarr_v2(url: str) -> ReferenceStoreT:
    """
    Scan a Zarr store in S3 and return Kerchunk-style references for all keys.

    Parameters
    ----------
    url : str
        URL to Zarr store. Must start with `s3://` and may include sub directories (e.g. `s3://foo/bar`)

    Returns
    -------
    refs : dict
        Kerchunk-style references for all keys in Zarr V2 store
    """
    import s3fs

    parsed_url = urlparse(url)
    if parsed_url.scheme != "s3":
        raise NotImplementedError(f"Only s3 urls are supported. Got {url}")

    store_prefix = f"{parsed_url.netloc}/{parsed_url.path[1:]}"  # [1:] skips leading slash
    if not store_prefix.endswith("/"):
        store_prefix += "/"  # add trailing slash (this will be removed from all keys below)

    # TODO: replace this workaround with more generic handling of S3 options
    storage_options = {}
    endpoint_url = config.get("s3.endpoint_url", None)
    if endpoint_url:
        storage_options = {"client_kwargs": {"endpoint_url": endpoint_url}}
    s3 = s3fs.S3FileSystem(**storage_options)

    store: ReferenceStoreT = {}
    for _, _, files in s3.walk(url, detail=True, topdown=True):
        for file_name, details in files.items():
            # For a provided `url` of `s3://bucket/foo/`
            # where walk finds a file such as `s3://bucket/foo/bar/.zattrs`
            # `file_name` is only the name of the file `.zattrs`
            # `key_path` is the complete path to the file `bucket/foo/bar/.zattrs`
            # `key` is relative to store_prefix of the url: `bar/.zattrs`
            key_path = details["name"]
            key = key_path.replace(store_prefix, "")

            # load metadata docs now
            if file_name in [".zattrs", ".zgroup", ".zarray"]:
                doc = json.loads(s3.cat(key_path))
                store[key] = doc

            # skip the .zmetadata (we don't need it)
            elif file_name == ".zmetadata":
                continue

            # use the info in from fs.walk to populate the reference
            elif is_v2_chunk_key(file_name):
                store[key] = [f"s3://{key_path}", 0, details["size"]]

            else:
                logger.warning(f"skipping unrecognized key: {key_path}")

    return store


def reformat_kerchunk_refs(refs: Dict[str, Any], new_path: Path) -> Tuple[Dict[Path, MetaDictT], Dict[Path, ReferenceData]]:
    """
    Reformat Kerchunk-style references to Zarr V3 / Arraylake references

    Parameters
    ----------
    refs : dict
        Mapping of references from Kerchunk (or similar)
    new_path : str
        Root path for reference data.

    Returns
    -------
    meta_docs : dict
        Metadata documents, reformatted to align with Arraylake specifications
    chunk_refs : dict
        Chunk references, reformatted to align with Arraylake specifications
    """
    meta_docs = {}  # type: Dict[Path, Dict]
    chunk_refs = {}  # type: Dict[Path, ReferenceData]

    if new_path.endswith("/"):
        new_path = new_path[:-1]

    refs = make_v3_store(refs)

    for k, v in refs.items():
        if k == "zarr.json":
            pass
        elif is_chunk_key(k):
            assert isinstance(v, list)
            new_key = Path(k.replace(data_root[:-1], data_root + new_path))
            chunk_refs[new_key] = ReferenceData(uri=v[0], offset=v[1], length=v[2], hash=None)  # type: ignore
        elif is_meta_key(k):
            assert isinstance(v, dict)
            new_key = Path(k.replace(meta_root[:-1], meta_root + new_path))
            meta_docs[new_key] = v

    return meta_docs, chunk_refs
