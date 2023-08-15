from getajob.utils import extract_pdf_text_by_url
from getajob.abstractions.models import Entity
from getajob.contexts.users.resumes.repository import ResumeRepository

from .suggestor import ResumeSuggestor


class ResumeSuggestorUnitOfWork:
    def __init__(self, resume_repo: ResumeRepository):
        self.resume_repo = resume_repo

    def create_resume_suggestion(self, user_id: str, resume_id: str) -> str:
        resume = self.resume_repo.get(
            resume_id, parent_collections={Entity.USERS.value: user_id}
        )
        resume_text = extract_pdf_text_by_url(resume.resume_url)
        return ResumeSuggestor(resume_text).provide_suggestion()
