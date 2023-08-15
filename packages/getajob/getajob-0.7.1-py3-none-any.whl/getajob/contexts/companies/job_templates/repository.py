from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection

from .models import JobTemplate


class JobTemplateRepository(MultipleChildrenRepository[JobTemplate]):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
    ):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.JOB_TEMPLATES.value,
                entity_model=JobTemplate,
            ),
            required_parent_keys=[Entity.COMPANIES.value],
        )
