from enum import Enum

from getajob.vendor.clerk.models import ClerkBaseModel, ClerkWebhookEvent


class ClerkCompanyWebhookType(str, Enum):
    organization_created = "organization.created"
    organization_deleted = "organization.deleted"
    organization_updated = "organization.updated"


class ClerkCompanyWebhookEvent(ClerkWebhookEvent):
    type: ClerkCompanyWebhookType


class ClerkCompany(ClerkBaseModel):
    created_at: int
    created_by: str
    image_url: str | None = None
    logo_url: str | None = None
    name: str
    public_metadata: dict = {}
    slug: str
    updated_at: int


class ClerkCompanyCreated(ClerkBaseModel):
    image_url: str | None = None
    logo_url: str | None = None
    name: str | None = None
    public_metadata: dict = {}
    slug: str | None = None
    updated_at: int | None = None


class ClerkCompanyDeleted(ClerkBaseModel):
    deleted: bool
