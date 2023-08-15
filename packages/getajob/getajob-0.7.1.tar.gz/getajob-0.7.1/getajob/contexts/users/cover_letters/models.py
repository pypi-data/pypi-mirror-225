from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class CreateCoverLetter(BaseModel):
    cover_letter: str


class UpdateCoverLetter(CreateCoverLetter):
    ...


class CoverLetter(CreateCoverLetter, BaseDataModel):
    cover_letter: str
