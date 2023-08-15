from .models import AdminDashboard
from .unit_of_work import AdminDashboardUnitOfWork


class AdminDashboardRepository:
    def __init__(self, *, request_scope):
        self.request_scope = request_scope

    async def get_admin_dashboard(self) -> AdminDashboard:
        return await AdminDashboardUnitOfWork(self.request_scope).get_admin_dashboard()
