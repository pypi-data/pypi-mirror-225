from fastapi import HTTPException

from getajob.abstractions.models import Entity
from getajob.abstractions.repository import BaseRepository
from getajob.contexts.users.resumes.repository import ResumeRepository
from getajob.contexts.companies.jobs.repository import JobsRepository
from getajob.contexts.applications.applicant_tracking.repository import ATSRepository
from getajob.contexts.applications.applicant_tracking.models import SetATSDetails
from getajob.vendor.firestore.models import FirestoreFilters

from .models import UserCreatedApplication, CreateApplication, Application


class ApplicationsUnitOfWork:
    def __init__(self, application_repo: BaseRepository):
        self.application_repo = application_repo

    def user_creates_application(
        self,
        user_id: str,
        resume_repo: ResumeRepository,
        job_repo: JobsRepository,
        applicant_tracking_repo: ATSRepository,
        create_application: UserCreatedApplication,
    ):
        # Check that the company and job is still viable
        job = job_repo.get(
            create_application.job_id,
            parent_collections={Entity.COMPANIES.value: create_application.company_id},
        )
        if job.position_filled:
            raise HTTPException(status_code=400, detail="Job has been filled")

        # Check that user hasn't already applied to this job
        user_application = self.application_repo.query(
            filters=[
                FirestoreFilters(field="user_id", operator="==", value=user_id),
                FirestoreFilters(
                    field="job_id", operator="==", value=create_application.job_id
                ),
            ]
        ).data
        if user_application:
            raise HTTPException(
                status_code=400, detail="You have already applied to this job"
            )

        # Check that resume exists
        assert resume_repo.get(
            parent_collections={Entity.USERS.value: user_id},
            doc_id=create_application.resume_id,
        )

        # Create the application
        application: Application = self.application_repo.create(
            data=CreateApplication(
                user_id=user_id,
                job_id=create_application.job_id,
                resume_id=create_application.resume_id,
                company_id=create_application.company_id,
            )
        )

        # Create the default application tracking details
        applicant_tracking_repo.set_sub_entity(
            data=SetATSDetails(),
            parent_collections={
                Entity.APPLICATIONS.value: application.id,
            },
        )
        return application
