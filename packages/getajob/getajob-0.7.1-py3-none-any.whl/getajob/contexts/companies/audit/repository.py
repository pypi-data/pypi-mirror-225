from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import (
    Entity,
    UserAndDatabaseConnection,
)

from .models import AuditLog


class AuditLogRepository(MultipleChildrenRepository[AuditLog]):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.COMPANY_AUDITS.value,
                entity_model=AuditLog,
            ),
            [Entity.COMPANIES.value],
        )

    def update(self, *args, **kwargs):
        raise NotImplementedError("Audit logs cannot be updated")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("Audit logs cannot be deleted")
