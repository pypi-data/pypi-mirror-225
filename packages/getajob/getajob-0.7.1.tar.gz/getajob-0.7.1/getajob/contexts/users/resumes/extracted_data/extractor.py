"""
This module is intended to take a PDF of a resume and extract the data from it.
"""

import json
import asyncio

from getajob.vendor.openai.repository import OpenAIRepository
from getajob.contexts.users.resumes.extracted_data.models import (
    SetExtractedResume,
    Qualifications,
    Education,
    WorkHistory,
    Language,
    Certificate,
    Project,
    Reference,
    VolunteerWork,
)


class ResumeExtractor:
    def __init__(self, resume_text: str):
        self.repo = OpenAIRepository()
        self.resume_text = resume_text

    async def _resume_extract_prompt(self, requested_information: dict):
        prompt = f"Given the following resume text, return in JSON format only the following information: {json.dumps(requested_information)}\n\n{self.resume_text}"
        results = self.repo.text_prompt(prompt, max_tokens=1000)
        try:
            return json.loads(results)
        except json.decoder.JSONDecodeError:
            return {}

    async def extract_contact_information(self):
        requested_information = {"name": "", "email": "", "phone": "", "address": ""}
        return await self._resume_extract_prompt(requested_information)

    async def extract_objective(self):
        json_template = {"objective": ""}
        return await self._resume_extract_prompt(json_template)

    async def extract_qualifications(self):
        json_template = {"qualifications": [{"years_experience": 0, "skills": []}]}
        return await self._resume_extract_prompt(json_template)

    async def extract_education(self):
        json_template = {
            "education": [
                {
                    "degree": "",
                    "major": "",
                    "minor": "",
                    "university": "",
                    "expected_graduation_date": "",
                    "gpa": "",
                }
            ]
        }
        return await self._resume_extract_prompt(json_template)

    async def extract_work_history(self):
        json_template = {
            "work_history": [
                {"position": "", "company": "", "time_period": "", "tasks": ["", ""]}
            ]
        }
        return await self._resume_extract_prompt(json_template)

    async def extract_languages(self):
        json_template = {"languages": [{"language": "", "proficiency": ""}]}
        return await self._resume_extract_prompt(json_template)

    async def extract_certificates(self):
        json_template = {"certificates": [{"name": "", "issuer": "", "date": ""}]}
        return await self._resume_extract_prompt(json_template)

    async def extract_projects(self):
        json_template = {
            "projects": [{"name": "", "description": "", "time_period": ""}]
        }
        return await self._resume_extract_prompt(json_template)

    async def extract_references(self):
        json_template = {
            "references": [{"name": "", "contact_details": "", "relation": ""}]
        }
        return await self._resume_extract_prompt(json_template)

    async def extract_volunteer_work(self):
        json_template = {
            "volunteer_work": [{"position": "", "organization": "", "time_period": ""}]
        }
        return await self._resume_extract_prompt(json_template)

    async def extract_all(self):
        data = {}
        tasks = [
            self.extract_contact_information(),
            self.extract_objective(),
            self.extract_qualifications(),
            self.extract_education(),
            self.extract_work_history(),
            self.extract_languages(),
            self.extract_certificates(),
            self.extract_projects(),
            self.extract_references(),
            self.extract_volunteer_work(),
        ]
        results = await asyncio.gather(*tasks)

        keys = [
            "contact_information",
            "objective",
            "qualifications",
            "education",
            "work_history",
            "languages",
            "certificates",
            "projects",
            "references",
            "volunteer_work",
        ]

        for key, result in zip(keys, results):
            data[key] = result

        return SetExtractedResume(
            name=data.get("contact_information", {}).get("name"),
            address=data.get("contact_information", {}).get("address"),
            phone=data.get("contact_information", {}).get("phone"),
            email=data.get("contact_information", {}).get("email"),
            objective=data.get("objective", {}).get("objective"),
            qualifications=[
                Qualifications(
                    YearsExperience=qualification.get("years_experience"),
                    Skills=qualification.get("skills"),
                )
                for qualification in data.get("qualifications", {}).get(
                    "qualifications", []
                )
            ],
            education=[
                Education(
                    Degree=education.get("degree"),
                    Major=education.get("major"),
                    Minor=education.get("minor"),
                    University=education.get("university"),
                    ExpectedGraduationDate=education.get("expected_graduation_date"),
                    GPA=education.get("gpa"),
                )
                for education in data.get("education", {}).get("education", [])
            ],
            work_history=[
                WorkHistory(
                    Position=work.get("position"),
                    Company=work.get("company"),
                    TimePeriod=work.get("time_period"),
                    tasks=work.get("tasks"),
                )
                for work in data.get("work_history", {}).get("work_history", [])
            ],
            languages=[
                Language(
                    Language=language.get("language"),
                    Proficiency=language.get("proficiency"),
                )
                for language in data.get("languages", {}).get("languages", [])
            ],
            certificates=[
                Certificate(
                    Name=certificate.get("name"),
                    Issuer=certificate.get("issuer"),
                    Date=certificate.get("date"),
                )
                for certificate in data.get("certificates", {}).get("certificates", [])
            ],
            projects=[
                Project(
                    Name=project.get("name"),
                    Description=project.get("description"),
                    TimePeriod=project.get("time_period"),
                )
                for project in data.get("projects", {}).get("projects", [])
            ],
            references=[
                Reference(
                    Name=reference.get("name"),
                    ContactDetails=reference.get("contact_details"),
                    Relation=reference.get("relation"),
                )
                for reference in data.get("references", {}).get("references", [])
            ],
            volunteer_work=[
                VolunteerWork(
                    Position=volunteer.get("position"),
                    Organization=volunteer.get("organization"),
                    TimePeriod=volunteer.get("time_period"),
                )
                for volunteer in data.get("volunteer_work", {}).get(
                    "volunteer_work", []
                )
            ],
        )
