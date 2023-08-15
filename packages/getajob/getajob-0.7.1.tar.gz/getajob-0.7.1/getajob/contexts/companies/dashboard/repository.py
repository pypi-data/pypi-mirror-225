from getajob.contexts.companies.jobs.repository import JobsRepository
from getajob.contexts.applications.repository import ApplicationRepository
from getajob.contexts.companies.saved_candidates.repository import (
    CompanySavesCandidateRepository,
)

from .models import CompanyDashboard
from .unit_of_work import CompanyDashboardUnitOfWork


class CompanyDashboardRepository:
    def __init__(self, *, request_scope):
        self.request_scope = request_scope

    def get_company_dashboard(self, company_id: str) -> CompanyDashboard:
        return CompanyDashboardUnitOfWork(
            JobsRepository(request_scope=self.request_scope, kafka=None),
            ApplicationRepository(request_scope=self.request_scope, kafka=None),
            CompanySavesCandidateRepository(request_scope=self.request_scope),
        ).get_company_dashboard(company_id)
