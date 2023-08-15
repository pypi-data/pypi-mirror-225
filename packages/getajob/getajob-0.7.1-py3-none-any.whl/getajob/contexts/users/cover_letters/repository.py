from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection

from .models import CoverLetter


class CoverLetterRepository(MultipleChildrenRepository[CoverLetter]):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.COVER_LETTERS.value,
                entity_model=CoverLetter,
            ),
            required_parent_keys=[Entity.USERS.value],
        )
