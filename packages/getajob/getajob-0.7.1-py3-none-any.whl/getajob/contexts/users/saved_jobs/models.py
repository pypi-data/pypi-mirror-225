from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel
from getajob.contexts.companies.jobs.models import Job


class UserSavedJob(BaseModel):
    company_id: str
    job_id: str


class SavedJob(UserSavedJob, BaseDataModel):
    job: Job | None = None
