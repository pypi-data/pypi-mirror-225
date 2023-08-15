from enum import Enum
from pydantic import BaseModel


class ClerkWebhookEvent(BaseModel):
    data: dict
    object: str
    type: Enum


class ClerkBaseModel(BaseModel):
    id: str
    object: str


class ClerkCompanyMemberType(str, Enum):
    admin = "admin"
    basic_member = "basic_member"


class ClerkInvitationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    revoked = "revoked"
