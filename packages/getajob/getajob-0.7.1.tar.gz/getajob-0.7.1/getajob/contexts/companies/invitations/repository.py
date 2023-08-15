from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection

from .models import RecruiterInvitation


class RecruiterInvitationsRepository(MultipleChildrenRepository[RecruiterInvitation]):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.RECRUITER_INVITATIONS.value,
                entity_model=RecruiterInvitation,
            ),
            required_parent_keys=[Entity.COMPANIES.value],
        )
