"""
Given resume text, provide some generic feedback on how to improve it.
"""

from getajob.contexts.users.resumes.repository import ResumeRepository
from getajob.abstractions.models import UserAndDatabaseConnection

from .unit_of_work import ResumeSuggestorUnitOfWork


class ResumeSuggestionRepository:
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
    ):
        self.request_scope = request_scope

    def create_resume_suggestions(self, user_id: str, resume_id: str) -> str:
        return ResumeSuggestorUnitOfWork(
            resume_repo=ResumeRepository(request_scope=self.request_scope),
        ).create_resume_suggestion(user_id, resume_id)
