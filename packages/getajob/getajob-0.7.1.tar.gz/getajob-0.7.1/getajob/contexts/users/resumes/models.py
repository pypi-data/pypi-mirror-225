from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class UserCreateResume(BaseModel):
    file_type: str
    file_name: str
    resume_data: bytes


class CreateResume(BaseModel):
    # The only thing that matters is the location of the resume, not the file details
    remote_file_path: str
    resume_url: str


class Resume(CreateResume, BaseDataModel):
    ...
