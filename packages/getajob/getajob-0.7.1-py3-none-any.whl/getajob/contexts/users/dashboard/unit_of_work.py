from getajob.abstractions.models import Entity
from getajob.vendor.firestore.models import FirestoreFilters
from getajob.abstractions.repository import ParentRepository, MultipleChildrenRepository

from .models import UserDashboard


class UserDashboardUnitOfWork:
    def __init__(
        self,
        application_repo: ParentRepository,
        saved_jobs_repo: MultipleChildrenRepository,
    ):
        self.application_repo = application_repo
        self.saved_jobs_repo = saved_jobs_repo

    def _get_user_application_count(self, user_id: str) -> int:
        return self.application_repo.get_count_from_collection(
            parent_collections={},
            filters=[FirestoreFilters(field="user_id", operator="==", value=user_id)],
        )

    def _get_user_saved_job_count(self, user_id: str) -> int:
        return self.saved_jobs_repo.get_count_from_collection(
            parent_collections={Entity.USERS.value: user_id},
        )

    def get_user_dashboard(self, user_id: str) -> UserDashboard:
        return UserDashboard(
            num_applications=self._get_user_application_count(user_id),
            num_saved_jobs=self._get_user_saved_job_count(user_id),
        )
