import datetime
from dataclasses import dataclass
from enum import Enum
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    NewType,
    Optional,
    Tuple,
    TypeVar,
    Union,
)
from uuid import UUID

from bson import ObjectId
from pydantic import AnyHttpUrl, AnyUrl, BaseModel, EmailStr, Field, SecretStr
from typing_extensions import TypedDict

# This type is used by pymongo. This subclass makes it work with pydantic
# https://github.com/mongodb-developer/mongodb-with-fastapi/blob/ef8e87de50ba87f6b26b2c37a410e3f5b8f7310c/app.py#L15-L28

T = TypeVar("T")


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# These are type aliases, which allow us to write e.g. Path instead of str. Since they can be used interchangeably,
# I'm not sure how useful they are.

CommitID = PyObjectId
Path = str
MetastoreUrl = Union[AnyUrl, AnyHttpUrl]

# These are used by mypy in static typing to ensure logical correctness but cannot be used at runtime for validation.
# They are more strict than the aliases; they have to be explicitly constructed.

SessionID = NewType("SessionID", str)
TagName = NewType("TagName", str)
BranchName = NewType("BranchName", str)

CommitHistory = Iterable[Tuple[CommitID, SessionID]]


class BulkCreateDocBody(BaseModel):
    session_id: str
    content: Mapping[str, Any]
    path: Path


class CollectionName(str, Enum):
    metadata = "metadata"
    chunks = "chunks"


class ChunkHash(TypedDict):
    method: str
    token: str


class SessionInfo(TypedDict):
    id: SessionID
    start_time: datetime.datetime
    base_commit: Optional[CommitID]
    branch: Optional[BranchName]


# These are the Pydantic models. They can be used for both validation and typing.
# Presumably it is considerably more expensive to use a BaseModel than just a dict.


class ModelWithID(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RepoCreateBody(BaseModel):
    name: str
    description: Optional[str] = None


class Repo(BaseModel):
    org: str
    name: str
    created: datetime.datetime
    description: Optional[str] = None


class Author(BaseModel):
    name: Optional[str] = None
    email: EmailStr


class NewCommit(BaseModel):
    session_id: SessionID
    session_start_time: datetime.datetime
    parent_commit: Optional[PyObjectId] = None
    commit_time: datetime.datetime
    author_name: Optional[str] = None
    author_email: EmailStr
    # TODO: add constraints once we drop python 3.8
    # https://github.com/pydantic/pydantic/issues/156
    message: str

    class Config:
        json_encoders = {ObjectId: str}


# TODO: remove duplication with NewCommit. Redefining these attributes works around this error:
# Definition of "Config" in base class "ModelWithID" is incompatible with definition in base class "NewCommit"
class Commit(ModelWithID):
    session_id: SessionID
    session_start_time: datetime.datetime
    parent_commit: Optional[PyObjectId] = None
    commit_time: datetime.datetime
    author_name: Optional[str]
    author_email: EmailStr
    # TODO: add constraints once we drop python 3.8
    # https://github.com/pydantic/pydantic/issues/156
    message: str

    def author_entry(self):
        if self.author_name:
            return f"{self.author_name} <{self.author_email}>"
        else:
            return f"<{self.author_email}>"


class Branch(BaseModel):
    id: BranchName = Field(alias="_id")
    commit_id: PyObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Tag(BaseModel):
    id: TagName = Field(alias="_id")
    commit_id: PyObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


@dataclass
class DocResponse:
    id: str  # not PyObjectId
    session_id: SessionID
    path: Path
    content: Optional[dict] = None
    deleted: bool = False

    def __post_init__(self):
        checks = [
            isinstance(self.id, str),
            # session_id: Cannot use isinstance() with NewType, so we use str
            isinstance(self.session_id, str),
            isinstance(self.path, Path),
            isinstance(self.deleted, bool),
            isinstance(self.content, dict) if self.content else True,
        ]
        if not all(checks):
            raise ValueError(f"Validation failed {self}, {checks}")


class DocSessionsResponse(ModelWithID):
    session_id: SessionID
    deleted: bool = False
    chunksize: int = 0


class SessionPathsResponse(ModelWithID):
    path: Path
    deleted: bool = False


class ReferenceData(BaseModel):
    uri: str
    offset: int
    length: int
    hash: Optional[ChunkHash] = None


class UpdateBranchBody(BaseModel):
    branch: BranchName
    new_commit: CommitID
    new_branch: bool = False
    base_commit: CommitID = None

    class Config:
        json_encoders = {ObjectId: str}


class OauthTokens(BaseModel):
    access_token: SecretStr
    id_token: SecretStr
    refresh_token: SecretStr
    expires_in: int
    token_type: str

    class Config:
        json_encoders = {SecretStr: lambda v: v.get_secret_value() if v else None}

    def dict(self, **kwargs):
        """custom dict method that decodes secrets"""
        tokens = super().dict(**kwargs)
        for k, v in tokens.items():
            if isinstance(v, SecretStr):
                tokens[k] = v.get_secret_value()
        return tokens


class OauthTokensResponse(OauthTokens):
    refresh_token: Optional[SecretStr] = None

    def dict(self, **kwargs):
        """custom dict that drops default values"""
        tokens = super().dict(**kwargs)
        # special case: drop refresh token if it is None
        if tokens.get("refresh_token", 1) is None:
            del tokens["refresh_token"]
        return tokens


class UserInfo(BaseModel):
    sub: UUID
    first_name: str
    family_name: str
    email: EmailStr
    username: str

    def as_author(self) -> Author:
        return Author(name=f"{self.first_name} {self.family_name}", email=self.email)


class ApiTokenInfo(BaseModel):
    id: str = Field(min_length=22, max_length=22)
    email: EmailStr
    expiration: int

    def as_author(self) -> Author:
        return Author(email=self.email)


class PathSizeResponse(BaseModel):
    path: Path
    number_of_chunks: int
    total_chunk_bytes: int


class Array(BaseModel):
    attributes: Dict[str, Any] = {}
    chunk_grid: Dict[str, Any] = {}
    chunk_memory_layout: str = None
    compressor: Union[Dict[str, Any], None] = None
    data_type: Union[str, Dict[str, Any]] = None
    fill_value: Any = None
    extensions: list = []
    shape: Tuple[int, ...] = None


# Utility to coerce Array data types to string version
def get_array_dtype(arr: Array) -> str:
    import numpy as np

    if isinstance(arr.data_type, str):
        return str(np.dtype(arr.data_type))
    elif isinstance(arr.data_type, dict):
        return str(arr.data_type["type"])
    else:
        raise ValueError(f"unexpected array type {type(arr.data_type)}")


class Tree(BaseModel):
    trees: Dict[str, "Tree"] = {}
    arrays: Dict[str, Array] = {}
    attributes: Dict[str, Any] = {}

    def _as_rich_tree(self, name: str = "/"):
        from rich.jupyter import JupyterMixin
        from rich.tree import Tree as _RichTree

        class RichTree(_RichTree, JupyterMixin):
            pass

        def _walk_and_format_tree(td: Tree, tree: RichTree) -> RichTree:
            for key, group in td.trees.items():
                branch = tree.add(f":file_folder: {key}")
                _walk_and_format_tree(group, branch)
            for key, arr in td.arrays.items():
                dtype = get_array_dtype(arr)
                tree.add(f":regional_indicator_a: {key} {arr.shape} {dtype}")
            return tree

        return _walk_and_format_tree(self, RichTree(name))

    def __rich__(self):
        return self._as_rich_tree()

    def _as_ipytree(self, name: str = ""):
        from ipytree import Node
        from ipytree import Tree as IpyTree

        def _walk_and_format_tree(td: Tree) -> List[Node]:
            nodes = []
            for key, group in td.trees.items():
                _nodes = _walk_and_format_tree(group)
                node = Node(name=key, nodes=_nodes)
                node.icon = "folder"
                node.opened = False
                nodes.append(node)
            for key, arr in td.arrays.items():
                dtype = get_array_dtype(arr)
                node = Node(name=f"{key} {arr.shape} {dtype}")
                node.icon = "table"
                node.opened = False
                nodes.append(node)
            return nodes

        nodes = _walk_and_format_tree(self)
        node = Node(name=name, nodes=nodes)
        node.icon = "folder"
        node.opened = True
        tree = IpyTree(nodes=[node])

        return tree

    def _repr_mimebundle_(self, **kwargs):
        try:
            _tree = self._as_ipytree(name="/")
        except ImportError:
            try:
                _tree = self._as_rich_tree(name="/")
            except ImportError:
                return repr(self)
        return _tree._repr_mimebundle_(**kwargs)
