import typing as t
from datetime import datetime
from pydantic import BaseModel

from getajob.abstractions.models import Location, BaseDataModel
from getajob.static.enumerations import LanguageEnum

from ..enumerations import (
    PayType,
    ScheduleType,
    ExperienceLevel,
    JobLocationType,
    ResumeRequirement,
    WeeklyScheduleType,
    ShiftType,
)


class Pay(BaseModel):
    pay_type: PayType
    pay_min: int
    pay_max: int
    exact_pay: t.Optional[int] = None
    includes_bonus: t.Optional[bool] = None
    includes_commission: t.Optional[bool] = None
    includes_equity: t.Optional[bool] = None
    includes_tips: t.Optional[bool] = None
    includes_vacation: t.Optional[bool] = None
    included_vacation_days: t.Optional[int] = None
    includes_relocation: t.Optional[bool] = None
    max_included_relocation_amount: t.Optional[int] = None
    includes_signing_bonus: t.Optional[bool] = None
    max_included_signing_bonus_amount: t.Optional[int] = None


class ApplicationSettings(BaseModel):
    let_candidates_contact_you_by_email: bool = True
    let_candidates_contact_you_by_phone: bool = True
    resume_requirement: ResumeRequirement = ResumeRequirement.required


class PositionCategory(BaseModel):
    category: str
    subcategories: t.List[str]


class JobSkill(BaseModel):
    skill_name: str
    must_have: bool


class ApplicationQuestion(BaseModel):
    question: str
    answer_choices: t.List[str]
    deal_breaker: bool


class UserCreateJob(BaseModel):
    position_title: str
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
    internal_reference_code: str | None = None
    job_associated_company_description: str | None = None

    application_settings: ApplicationSettings | None = None
    application_questions: t.List[ApplicationQuestion] | None = None
    desired_start_date: datetime | None = None

    best_number_for_candidate_to_call: str | None = None
    is_draft: bool = True
    is_live: bool = False

    def get_required_fields_for_posting(self) -> t.List[str]:
        # TASK update is_draft, is_live etc. and checking the required fields
        return [
            "position_title",
            "description",
            "schedule",
            "location_type",
            "required_job_skills",
            "pay",
            "background_check_required",
            "drug_test_required",
            "years_of_experience",
        ]


class CreateJob(UserCreateJob):
    view_count: int = 0


class UpdateJob(UserCreateJob):
    position_title: str | None = None  # type: ignore


class InternalUpdateJob(UpdateJob):
    position_filled: t.Optional[bool] = None
    view_count: t.Optional[int] = None


class Job(CreateJob, BaseDataModel):
    position_filled: bool = False


class KafkaJob(Job):
    company_id: str
