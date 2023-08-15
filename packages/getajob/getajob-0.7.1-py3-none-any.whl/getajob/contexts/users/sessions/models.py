import typing as t
from pydantic import BaseModel

from getajob.abstractions.models import UserAndDatabaseConnection
from getajob.vendor.clerk.recruiters.models import ClerkCompanyMembership


class SessionData(BaseModel):
    email: str
    exp: int
    id: str
    name: str
    sid: t.Optional[str] = None
    sub: t.Optional[str] = None
    phone: t.Optional[str] = None
    memberships: t.Optional[t.List[ClerkCompanyMembership]] = None
    request_scope: t.Any | None = None
