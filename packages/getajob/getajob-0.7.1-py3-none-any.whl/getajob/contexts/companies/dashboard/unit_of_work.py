from getajob.abstractions.models import Entity
from getajob.vendor.firestore.models import FirestoreFilters
from getajob.abstractions.repository import MultipleChildrenRepository, ParentRepository

from .models import CompanyDashboard


class CompanyDashboardUnitOfWork:
    def __init__(
        self,
        job_repo: MultipleChildrenRepository,
        application_repo: ParentRepository,
        saved_candidate_repo: MultipleChildrenRepository,
    ):
        self.job_repo = job_repo
        self.application_repo = application_repo
        self.saved_candidate_repo = saved_candidate_repo

    def _get_num_live_jobs(self, company_id: str) -> int:
        return self.job_repo.get_count_from_collection(
            parent_collections={Entity.COMPANIES.value: company_id},
            filters=[FirestoreFilters(field="is_live", operator="==", value=True)],
        )

    def _get_number_of_applicants(self, company_id: str) -> int:
        return self.application_repo.get_count_from_collection(
            parent_collections={},
            filters=[
                FirestoreFilters(field="company_id", operator="==", value=company_id)
            ],
        )

    def _get_number_of_saved_candidates(self, company_id: str) -> int:
        return self.saved_candidate_repo.get_count_from_collection(
            parent_collections={Entity.COMPANIES.value: company_id},
        )

    def get_company_dashboard(self, company_id: str) -> CompanyDashboard:
        return CompanyDashboard(
            num_live_jobs=self._get_num_live_jobs(company_id),
            num_applicants=self._get_number_of_applicants(company_id),
            num_saved_candidates=self._get_number_of_saved_candidates(company_id),
        )
