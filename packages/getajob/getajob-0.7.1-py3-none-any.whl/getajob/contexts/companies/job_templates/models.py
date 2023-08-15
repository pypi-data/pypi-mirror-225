import typing as t
from pydantic import BaseModel

from getajob.abstractions.models import Location, BaseDataModel
from getajob.static.enumerations import LanguageEnum

from ..jobs.models import (
    PositionCategory,
    JobSkill,
    Pay,
    ApplicationSettings,
    ApplicationQuestion,
)
from ..enumerations import (
    ScheduleType,
    ExperienceLevel,
    JobLocationType,
    WeeklyScheduleType,
    ShiftType,
)


class CreateJobTemplate(BaseModel):
    position_title: str | None = None
    description: str | None = None
    position_category: PositionCategory | None = None
    schedule: ScheduleType | None = None
    years_of_experience: ExperienceLevel | None = None

    location_type: JobLocationType | None = None
    location: Location | None = None

    num_candidates_required: int | None = None
    ongoing_recruitment: bool | None = None

    required_job_skills: t.List[JobSkill] | None = None
    on_job_training_offered: bool | None = None

    weekly_day_range: t.List[WeeklyScheduleType] | None = None
    shift_type: t.List[ShiftType] | None = None

    pay: Pay | None = None

    language_requirements: t.List[LanguageEnum] | None = None

    background_check_required: bool | None = None
    drug_test_required: bool | None = None
    felons_accepted: bool | None = None
    disability_accepted: bool | None = None

    ideal_days_to_hire: int | None = None
    job_associated_company_description: str | None = None

    application_settings: ApplicationSettings | None = None
    application_questions: t.List[ApplicationQuestion] | None = None


class JobTemplate(BaseDataModel, CreateJobTemplate):
    ...
