from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class UserCreateChat(BaseModel):
    applicant_user_id: str
    recruiter_user_id: str
    company_id: str
    application_id: str


class Chat(UserCreateChat, BaseDataModel):
    ...
