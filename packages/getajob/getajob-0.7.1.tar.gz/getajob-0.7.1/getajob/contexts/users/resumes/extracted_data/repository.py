"""
Stores the results of data extraction as a single child under a given resume
"""

from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.contexts.users.resumes.repository import ResumeRepository
from getajob.abstractions.models import Entity, UserAndDatabaseConnection

from .models import GetExtractedResume
from .unit_of_work import ResumeExtractorUnitOfWork


class ResumeExtractionRepository(SingleChildRepository[GetExtractedResume]):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
    ):
        self.request_scope = request_scope
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.USER_DETAILS.value,
                entity_model=GetExtractedResume,
            ),
            required_parent_keys=[Entity.USERS.value, Entity.RESUMES.value],
        )

    async def create_resume_extraction(self, user_id: str, resume_id: str):
        return await ResumeExtractorUnitOfWork(
            resume_repo=ResumeRepository(request_scope=self.request_scope),
            resume_extraction_repo=self,
        ).create_resume_extraction(user_id, resume_id)
