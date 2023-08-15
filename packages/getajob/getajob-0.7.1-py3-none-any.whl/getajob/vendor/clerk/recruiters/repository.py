from getajob.abstractions.models import Entity, UserAndDatabaseConnection
from getajob.contexts.companies.recruiters.repository import RecruiterRepository
from getajob.contexts.companies.recruiters.recruiter_settings.repository import (
    RecruiterDetailsRepository,
)
from getajob.contexts.companies.recruiters.recruiter_settings.models import (
    SetRecruiterDetails,
)

from .models import (
    ClerkCompanyMembershipWebhookEvent,
    ClerkCompanyMembership,
    ClerkCompanyMembershipWebhookType,
    ClerkUpdateCompanyMembership,
    ClerkCompanyMember,
    UpdateClerkCompanyMemberWithRole,
)


class WebhookCompanyMembershipRepository:
    def __init__(self, request_scope: UserAndDatabaseConnection):
        self.repo = RecruiterRepository(request_scope=request_scope)
        self.request_scope = request_scope

    def handle_webhook_event(self, event: ClerkCompanyMembershipWebhookEvent):
        event_dict = {
            ClerkCompanyMembershipWebhookType.organization_membership_created: self.create_recruiter,
            ClerkCompanyMembershipWebhookType.organization_membership_updated: self.update_recruiter,
            ClerkCompanyMembershipWebhookType.organization_membership_deleted: self.delete_recruiter,
        }
        return event_dict[event.type](event)

    def _create_recruiter_details(self, company_id: str, recruiter_id: str):
        RecruiterDetailsRepository(request_scope=self.request_scope).set_sub_entity(
            data=SetRecruiterDetails(),
            parent_collections={
                Entity.COMPANIES.value: company_id,
                Entity.RECRUITERS.value: recruiter_id,
            },
        )

    def create_recruiter(self, event: ClerkCompanyMembershipWebhookEvent):
        create_event = ClerkCompanyMembership(**event.data)
        recruiter = ClerkCompanyMember(
            **create_event.public_user_data.dict(),
            id=create_event.id,
            role=create_event.role
        )
        recruiter = self.repo.create(
            data=recruiter,
            provided_id=create_event.id,
            parent_collections={Entity.COMPANIES.value: create_event.organization.id},
        )
        self._create_recruiter_details(
            company_id=create_event.organization.id, recruiter_id=create_event.id
        )
        return recruiter

    def delete_recruiter(self, event: ClerkCompanyMembershipWebhookEvent):
        delete_event = ClerkUpdateCompanyMembership(**event.data)
        return self.repo.delete(
            doc_id=delete_event.id,
            parent_collections={Entity.COMPANIES.value: delete_event.organization.id},
        )

    def update_recruiter(self, event: ClerkCompanyMembershipWebhookEvent):
        update_event = ClerkUpdateCompanyMembership(**event.data)
        recruiter = UpdateClerkCompanyMemberWithRole(
            **update_event.public_user_data.dict(), role=update_event.role
        )
        return self.repo.update(
            doc_id=update_event.id,
            data=recruiter,
            parent_collections={Entity.COMPANIES.value: update_event.organization.id},
        )
