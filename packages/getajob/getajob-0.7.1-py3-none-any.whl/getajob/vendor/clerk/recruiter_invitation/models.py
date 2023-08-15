from enum import Enum

from getajob.vendor.clerk.models import (
    ClerkBaseModel,
    ClerkWebhookEvent,
    ClerkCompanyMemberType,
    ClerkInvitationStatus,
)


class ClerkCompanyInvitationsWebhookType(str, Enum):
    organization_invitation_created = "organizationInvitation.created"
    organization_invitation_revoked = "organizationInvitation.revoked"
    organization_invitation_accepted = "organizationInvitation.accepted"


class ClerkCompanyInvitationsWebhookEvent(ClerkWebhookEvent):
    type: ClerkCompanyInvitationsWebhookType


class ClerkCompanyInvitation(ClerkBaseModel):
    created_at: int
    email_address: str
    organization_id: str
    role: ClerkCompanyMemberType
    status: ClerkInvitationStatus
    updated_at: int
