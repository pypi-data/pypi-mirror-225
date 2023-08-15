from typing import List
from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class Qualifications(BaseModel):
    YearsExperience: int | None = None
    Skills: List[str] | None = None


class Education(BaseModel):
    Degree: str | None = None
    Major: str | None = None
    Minor: str | None = None
    University: str | None = None
    ExpectedGraduationDate: str | None = None
    GPA: str | None = None


class WorkHistory(BaseModel):
    Position: str | None = None
    Company: str | None = None
    TimePeriod: str | None = None
    tasks: List[str] | None = None


class Language(BaseModel):
    Language: str | None = None
    Proficiency: str | None = None


class Certificate(BaseModel):
    Name: str | None = None
    Issuer: str | None = None
    Date: str | None = None


class Project(BaseModel):
    Name: str | None = None
    Description: str | None = None
    TimePeriod: str | None = None


class Reference(BaseModel):
    Name: str | None = None
    ContactDetails: str | None = None
    Relation: str | None = None


class VolunteerWork(BaseModel):
    Position: str | None = None
    Organization: str | None = None
    TimePeriod: str | None = None


class SetExtractedResume(BaseModel):
    name: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    objective: str | None = None
    skills: List[str] | None = None
    qualifications: List[Qualifications] | None = None
    education: List[Education] | None = None
    work_history: List[WorkHistory] | None = None
    languages: List[Language] | None = None
    certificates: List[Certificate] | None = None
    projects: List[Project] | None = None
    references: List[Reference] | None = None
    volunteer_work: List[VolunteerWork] | None = None
    hobbies: List[str] | None = None
    links: List[str] | None = None


class GetExtractedResume(BaseDataModel, SetExtractedResume):
    ...
