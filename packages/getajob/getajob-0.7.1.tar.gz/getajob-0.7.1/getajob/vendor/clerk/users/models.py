from enum import Enum

from getajob.vendor.clerk.models import ClerkBaseModel, ClerkWebhookEvent


class ClerkUserWebhookType(str, Enum):
    user_created = "user.created"
    user_deleted = "user.deleted"
    user_updated = "user.updated"


class ClerkUserWebhookEvent(ClerkWebhookEvent):
    type: ClerkUserWebhookType


class ClerkUserEmailAddresses(ClerkBaseModel):
    email_address: str
    linked_to: list
    verification: dict


class ClertkUserPhoneNumbers(ClerkBaseModel):
    linked_to: list
    phone_number: str
    verification: dict


class ClerkUser(ClerkBaseModel):
    created_at: int
    primary_email_address_id: str
    email_addresses: list[ClerkUserEmailAddresses]
    phone_numbers: list[ClertkUserPhoneNumbers]
    first_name: str
    last_name: str
    gender: str
    external_id: str | None = None
    birthday: str
    image_url: str | None = None


class ClerkWebhookUserUpdated(ClerkBaseModel):
    primary_email_address_id: str | None = None
    email_addresses: list[ClerkUserEmailAddresses] | None = None
    phone_numbers: list[ClertkUserPhoneNumbers] | None = None
    first_name: str | None = None
    last_name: str | None = None
    gender: str | None = None
    external_id: str | None = None
    birthday: str | None = None
    updated_at: int


class ClerkWebhookUserDeleted(ClerkBaseModel):
    deleted: bool
