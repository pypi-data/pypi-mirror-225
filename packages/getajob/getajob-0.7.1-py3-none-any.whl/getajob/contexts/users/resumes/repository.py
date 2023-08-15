from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection
from getajob.vendor.firebase_storage.repository import FirebaseStorageRepository

from .models import Resume, UserCreateResume
from .unt_of_work import ResumeUnitOfWork


class ResumeRepository(MultipleChildrenRepository[Resume]):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.RESUME_EXTRACTED_DATA.value,
                entity_model=Resume,
            ),
            required_parent_keys=[Entity.USERS.value],
        )

    def create_resume(
        self,
        user_id: str,
        data: UserCreateResume,
        storage_repo: FirebaseStorageRepository,
    ):
        return ResumeUnitOfWork(self, storage_repo).create_user_resume(user_id, data)

    def delete_resume(
        self, user_id: str, resume_id: str, storage_repo: FirebaseStorageRepository
    ):
        return ResumeUnitOfWork(self, storage_repo).delete_user_resume(
            user_id, resume_id
        )

    def update_resume(
        self,
        user_id: str,
        resume_id: str,
        data: UserCreateResume,
        storage_repo: FirebaseStorageRepository,
    ):
        return ResumeUnitOfWork(self, storage_repo).update_user_resume(
            user_id, resume_id, data
        )
