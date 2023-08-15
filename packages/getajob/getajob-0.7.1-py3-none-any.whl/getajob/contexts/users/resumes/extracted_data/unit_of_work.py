from getajob.utils import extract_pdf_text_by_url
from getajob.abstractions.models import Entity
from getajob.abstractions.repository import (
    SingleChildRepository,
    MultipleChildrenRepository,
)

from .extractor import ResumeExtractor


class ResumeExtractorUnitOfWork:
    def __init__(
        self,
        resume_repo: MultipleChildrenRepository,
        resume_extraction_repo: SingleChildRepository,
    ):
        self.resume_repo = resume_repo
        self.resume_extraction_repo = resume_extraction_repo

    async def create_resume_extraction(self, user_id: str, resume_id: str):
        resume = self.resume_repo.get(
            resume_id, parent_collections={Entity.USERS.value: user_id}
        )
        resume_text = extract_pdf_text_by_url(resume.resume_url)
        return await ResumeExtractor(resume_text).extract_all()
