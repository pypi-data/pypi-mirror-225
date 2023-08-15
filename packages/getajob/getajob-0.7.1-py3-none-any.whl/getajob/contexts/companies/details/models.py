import typing as t
from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel

from ..enumerations import NumEmployeesEnum, Benefits


class SetCompanyDetails(BaseModel):
    num_employees: NumEmployeesEnum | None = None
    owner_first_and_last_name: str | None = None
    owner_phone_number: str | None = None
    company_description: str | None = None
    company_website_link: str | None = None
    why_candidates_should_work_here: str | None = None

    company_benefits: list[Benefits | str] | None = None

    company_main_image_url: str | None = None
    company_additional_image_urls: t.List[str] | None = None


class CompanyDetails(BaseDataModel, SetCompanyDetails):
    ...
