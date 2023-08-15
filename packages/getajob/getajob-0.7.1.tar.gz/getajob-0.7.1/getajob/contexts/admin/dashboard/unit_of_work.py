from getajob.abstractions.models import Entity
from getajob.abstractions.repository import (
    get_count_from_collection,
    get_count_from_subcollection,
)

from .models import AdminDashboard


class AdminDashboardUnitOfWork:
    def __init__(self, request_scope):
        self.request_scope = request_scope

    async def _get_total_users(self) -> int:
        return get_count_from_collection(self.request_scope.db, Entity.USERS.value)

    async def _get_total_applications(self) -> int:
        return get_count_from_collection(
            self.request_scope.db, Entity.APPLICATIONS.value
        )

    async def _get_total_companies(self) -> int:
        return get_count_from_collection(self.request_scope.db, Entity.COMPANIES.value)

    async def _get_total_jobs(self) -> int:
        return get_count_from_subcollection(self.request_scope.db, Entity.JOBS.value)

    async def get_admin_dashboard(self) -> AdminDashboard:
        return AdminDashboard(
            total_users=await self._get_total_users(),
            total_applications=await self._get_total_applications(),
            total_companies=await self._get_total_companies(),
            total_jobs=await self._get_total_jobs(),
        )
