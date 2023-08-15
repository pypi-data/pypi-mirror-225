import typing as t
from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel
from getajob.contexts.users.models import User
from getajob.contexts.companies.jobs.models import Job
from getajob.contexts.users.details.models import UserDetails

from .applicant_tracking.models import ATSDetails
from .enumerations import ApplicationStatus, CompanyQuickAction


class UserCreatedApplication(BaseModel):
    company_id: str
    job_id: str
    resume_id: str
    cover_letter_content: t.Optional[str] = None


class CreateApplication(UserCreatedApplication):
    user_id: str
    application_status: ApplicationStatus = ApplicationStatus.submitted


class UpdateApplication(BaseModel):
    application_status: ApplicationStatus | None = None


class Application(CreateApplication, BaseDataModel):
    ...


class ApplicationSearch(BaseDataModel):
    """
    This model is created an updated based on applications created
    """

    user_id: str
    company_id: str
    job_id: str
    user: User
    user_details: UserDetails
    job: Job
    application: Application
    application_ats: ATSDetails

    user_is_deleted: bool = False  # Caused by a user deleting their account
    job_is_deleted: bool = False  # Caused by a company deleting a job
    job_is_filled: bool = False  # Caused by a company filling a job
    is_deleted: bool = False  # Soft delete when application is deleted


class CompanyQueryApplications(BaseModel):
    company_id: str
    job_id: str | None = None
    is_viewed: bool | None = None
    quick_action_status: CompanyQuickAction | None = None
    tags: list[str] | None = None

    page: int = 0
    hits_per_page: int = 20


class UserQueryApplications(BaseModel):
    user_id: str
    company_id: str | None = None
    job_id: str | None = None

    page: int = 0
    hits_per_page: int = 20


class UserQueryApplicationsResult(BaseModel):
    company_id: str
    job: Job
    application: Application
