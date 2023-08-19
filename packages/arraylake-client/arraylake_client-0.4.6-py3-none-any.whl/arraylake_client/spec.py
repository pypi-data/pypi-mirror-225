from typing import Dict, List, Tuple, TypedDict, Union

MongoDBIndex = Union[str, Tuple[Tuple[str, int], ...]]


class CollectionSpec(TypedDict):
    NAME: str
    INDEXES: List[MongoDBIndex]


class IcechunkSpec(TypedDict):
    VERSION: int
    METADATA_COLLECTION_NAME: str
    METADATA_DOCUMENT_ID: str
    CHUNKSTORE_KEY: str
    COLLECTIONS: Dict[str, CollectionSpec]


ICECHUNK_SPEC: IcechunkSpec = {
    "VERSION": 1,
    "METADATA_COLLECTION_NAME": "icechunk_metadata",
    "METADATA_DOCUMENT_ID": "root",
    "CHUNKSTORE_KEY": "chunkstore_uri",
    "COLLECTIONS": {
        "COMMITS": {"NAME": "commits", "INDEXES": []},
        "metadata": {
            "NAME": "metadata",
            "INDEXES": [
                "session_id",
                (("session_id", 1), ("path", 1), ("deleted", 1), ("_id", -1)),
            ],
        },
        "chunks": {
            "NAME": "chunk_manifest",
            "INDEXES": [
                "session_id",
                (("path", 1), ("session_id", 1)),
                (("session_id", 1), ("path", 1), ("deleted", 1), ("_id", -1)),
            ],
        },
        "TAGS": {"NAME": "tags", "INDEXES": []},
        "BRANCHES": {"NAME": "branches", "INDEXES": []},
    },
}
