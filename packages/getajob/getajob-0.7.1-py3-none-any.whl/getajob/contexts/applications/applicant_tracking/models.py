"""
This module allows for users to track applications throughout different stages

They can define their own stages, attach notes and documents to an applicant

Tracking will be queried by company and job
It will join user information and user details

It will allow recruiters to add tags and statuses to applicants

"""
from pydantic import BaseModel
from getajob.abstractions.models import BaseDataModel


from ..enumerations import CompanyQuickAction


class SetATSDetails(BaseModel):
    is_viewed: bool = False
    quick_action_status: CompanyQuickAction | None = None
    ats_status: str | None = None
    notes: str | None = None
    tags: list[str] | None = None


class ATSDetails(SetATSDetails, BaseDataModel):
    ...
