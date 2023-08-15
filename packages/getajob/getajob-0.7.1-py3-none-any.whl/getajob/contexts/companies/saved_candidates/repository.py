from typing import cast
from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection
from getajob.contexts.users.repository import UserRepository
from getajob.contexts.users.models import User

from .models import SavedCandidate


class CompanySavesCandidateRepository(MultipleChildrenRepository[SavedCandidate]):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.COMPANY_SAVES_CANDIDATES.value,
                entity_model=SavedCandidate,
            ),
            required_parent_keys=[Entity.COMPANIES.value],
        )
        self.request_scope = request_scope

    def _get_user_ids(self, saved_candidates: list[SavedCandidate]) -> list[str]:
        return [user_saved_job.user_id for user_saved_job in saved_candidates]

    def _get_users_as_dict(self, user_ids: list[str], request_scope) -> dict[str, User]:
        user_details_repo = UserRepository(request_scope=request_scope, kafka=None)
        users = user_details_repo.get_all(
            items_to_get=user_ids, parent_collections={}
        ).data
        return {user.id: cast(User, user) for user in users}

    def _create_saved_candidates(
        self, saved_candidates: list[SavedCandidate], users_as_dict: dict
    ) -> list[SavedCandidate]:
        return [
            SavedCandidate(
                **saved_candidate.dict(exclude={"user"}),
                user=users_as_dict.get(saved_candidate.user_id)
            )
            for saved_candidate in saved_candidates
        ]

    def get_joined_saved_candidates(self, company_id: str) -> list[SavedCandidate]:
        saved_candidates: list[SavedCandidate] = self.query(
            parent_collections={Entity.COMPANIES.value: company_id}
        ).data
        user_ids = self._get_user_ids(saved_candidates)
        users_as_dict = self._get_users_as_dict(user_ids, self.request_scope)
        return self._create_saved_candidates(saved_candidates, users_as_dict)
