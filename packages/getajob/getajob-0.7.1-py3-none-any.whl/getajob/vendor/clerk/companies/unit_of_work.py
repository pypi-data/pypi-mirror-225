from getajob.abstractions.models import Entity
from getajob.contexts.companies.details.models import SetCompanyDetails
from getajob.contexts.companies.details.repository import CompanyDetailsRepository
from getajob.abstractions.repository import ParentRepository
from getajob.contexts.companies.applicant_tracking_settings.repository import (
    CompanyATSConfigRepository,
)
from getajob.contexts.companies.applicant_tracking_settings.models import SetATSConfig

from .models import (
    ClerkCompanyWebhookEvent,
    ClerkCompany,
)


class ClerkCompanyUnitOfWork:
    def __init__(self, request_scope):
        self.request_scope = request_scope

    def _create_default_company_ats_config(self, company_id: str):
        CompanyATSConfigRepository(request_scope=self.request_scope).set_sub_entity(
            data=SetATSConfig(),
            parent_collections={Entity.COMPANIES.value: company_id},
        )

    def _create_default_company_details(self, company_id: str):
        CompanyDetailsRepository(
            request_scope=self.request_scope, kafka=None
        ).set_sub_entity(
            data=SetCompanyDetails(),
            parent_collections={Entity.COMPANIES.value: company_id},
        )

    def create_new_company(
        self,
        webhook_repository: ParentRepository,
        event: ClerkCompanyWebhookEvent,
    ) -> ClerkCompany:
        create_event = ClerkCompany(**event.data)
        res = webhook_repository.create(data=create_event, provided_id=create_event.id)
        self._create_default_company_details(company_id=create_event.id)
        self._create_default_company_ats_config(company_id=create_event.id)
        return res
