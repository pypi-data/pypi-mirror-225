from getajob.contexts.companies.invitations.repository import (
    RecruiterInvitationsRepository,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection

from .models import (
    ClerkCompanyInvitation,
    ClerkCompanyInvitationsWebhookEvent,
    ClerkCompanyInvitationsWebhookType,
)


class WebhookCompanyInvitationRepository:
    def __init__(self, request_scope: UserAndDatabaseConnection):
        self.repo = RecruiterInvitationsRepository(request_scope=request_scope)

    def handle_webhook_event(self, event: ClerkCompanyInvitationsWebhookEvent):
        event_dict = {
            ClerkCompanyInvitationsWebhookType.organization_invitation_created: self.create_invitation,
            ClerkCompanyInvitationsWebhookType.organization_invitation_revoked: self.revoke_invitation,
            ClerkCompanyInvitationsWebhookType.organization_invitation_accepted: self.accept_invitation,
        }
        return event_dict[event.type](event)

    def create_invitation(self, event: ClerkCompanyInvitationsWebhookEvent):
        create_event = ClerkCompanyInvitation(**event.data)
        return self.repo.create(
            data=create_event,
            provided_id=create_event.id,
            parent_collections={Entity.COMPANIES.value: create_event.organization_id},
        )

    def revoke_invitation(self, event: ClerkCompanyInvitationsWebhookEvent):
        update_event = ClerkCompanyInvitation(**event.data)
        return self.repo.update(
            doc_id=update_event.id,
            data=update_event,
            parent_collections={Entity.COMPANIES.value: update_event.organization_id},
        )

    def accept_invitation(self, event: ClerkCompanyInvitationsWebhookEvent):
        update_event = ClerkCompanyInvitation(**event.data)
        return self.repo.update(
            doc_id=update_event.id,
            data=update_event,
            parent_collections={Entity.COMPANIES.value: update_event.organization_id},
        )
