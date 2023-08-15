from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel
from getajob.contexts.users.models import User


class CompanySavesCandidate(BaseModel):
    user_id: str
    saved_for_job_id: str | None = None


class SavedCandidate(CompanySavesCandidate, BaseDataModel):
    user: User | None = None
