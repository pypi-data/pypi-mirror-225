from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection

from .models import RecruiterDetails


class RecruiterDetailsRepository(SingleChildRepository[RecruiterDetails]):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
    ):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.RECRUITER_DETAILS.value,
                entity_model=RecruiterDetails,
            ),
            required_parent_keys=[
                Entity.COMPANIES.value,
                Entity.RECRUITERS.value,
            ],
        )
