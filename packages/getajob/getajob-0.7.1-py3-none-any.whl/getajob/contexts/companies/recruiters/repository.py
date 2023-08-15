from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection

from .models import Recruiter


class RecruiterRepository(MultipleChildrenRepository[Recruiter]):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.RECRUITERS.value,
                entity_model=Recruiter,
            ),
            required_parent_keys=[Entity.COMPANIES.value],
        )
