import typing as t
from pydantic import BaseModel

from getajob.config.settings import SETTINGS


class FirestorePagination(BaseModel):
    start_after: t.Optional[dict] = None
    limit: int = SETTINGS.DEFAULT_PAGE_LIMIT

    class Config:
        arbitrary_types_allowed = True


class FirestoreFilters(BaseModel):
    field: str
    operator: t.Literal[
        "==",
        ">",
        "<",
        ">=",
        "<=",
        "array-contains",
        "in",
        "array-contains-any",
        "not-in",
        "like",  # The like operator is custom soft text
    ]
    value: t.Any


class FirestoreOrderBy(BaseModel):
    field: str
    direction: t.Literal["ASCENDING", "DESCENDING"]


class FirestoreDocument(BaseModel):
    id: str
    data: t.Dict[str, t.Any]


class FirestorePaginatedResponse(BaseModel):
    results: t.List[FirestoreDocument]
    start_after: t.Optional[dict] = None
    count: int = 0

    class Config:
        arbitrary_types_allowed = True


class ParentAndCollection(BaseModel):
    parents: dict
    collection: str
    id: str
