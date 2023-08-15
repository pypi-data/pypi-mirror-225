"""
These are the models stored in Algolia for searching. 
They are built and maintained by the event stream through the services code repository.
"""

from getajob.abstractions.models import BaseDataModel
from getajob.contexts.companies.models import Company
from getajob.contexts.companies.details.models import CompanyDetails
from getajob.contexts.companies.jobs.models import Job
from getajob.contexts.users.details.models import UserDetails
from getajob.contexts.users.models import User
from getajob.contexts.applications.models import Application
from getajob.contexts.applications.applicant_tracking.models import ATSDetails


class CandidateSearch(BaseDataModel):
    """A generic search across all users and their details"""

    user: User
    user_details: UserDetails | None = None
    thumbnail: str | None = None

    is_deleted: bool = False  # Soft delete flag


class ApplicantSearch(BaseDataModel):
    """
    A Search for within a company to view all applicants for their jobs

    For now, user details are updated to reflect the latest changes, we are not
    storing the user details at the time of application differently.
    """

    user_id: str
    user: User
    user_details: UserDetails
    application: Application
    ats_details: ATSDetails
    company_id: str
    job_id: str

    is_deleted: bool = False  # Soft delete flag


class JobSearch(BaseDataModel):
    """The public facing job search tool"""

    job: Job
    company_id: str

    is_deleted: bool = False  # Soft delete flag


class CompanySearch(BaseDataModel):
    """The public facing company search tool"""

    company: Company
    company_details: CompanyDetails | None = None

    is_deleted: bool = False  # Soft delete flag
