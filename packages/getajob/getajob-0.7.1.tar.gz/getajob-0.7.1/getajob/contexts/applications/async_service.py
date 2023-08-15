from typing import cast
from datetime import datetime

from getajob.abstractions.models import Entity, ProcessedAsyncMessage
from getajob.contexts.users.repository import UserRepository
from getajob.contexts.users.details.repository import UserDetailsRepository
from getajob.contexts.companies.jobs.repository import JobsRepository
from getajob.contexts.applications.applicant_tracking.repository import ATSRepository
from getajob.contexts.applications.applicant_tracking.models import ATSDetails
from getajob.vendor.algolia.repository import AlgoliaSearchRepository

from .models import Application, ApplicationSearch


class AsyncronousApplicationService:
    def __init__(
        self,
        algolia_applications: AlgoliaSearchRepository,
    ):
        self.algolia_applications = algolia_applications

    async def create_application(self, processed_message: ProcessedAsyncMessage):
        application = cast(Application, processed_message.data)
        user = UserRepository(
            request_scope=processed_message.request_scope, kafka=None
        ).get(application.user_id)
        user_details = UserDetailsRepository(
            request_scope=processed_message.request_scope, kafka=None
        ).get_sub_entity(parent_collections={Entity.USERS.value: application.user_id})
        job = JobsRepository(
            request_scope=processed_message.request_scope, kafka=None
        ).get(
            application.job_id,
            parent_collections={
                Entity.COMPANIES.value: application.company_id,
            },
        )
        application_ats = ATSRepository(
            request_scope=processed_message.request_scope, kafka=None
        ).get_sub_entity(parent_collections={Entity.APPLICATIONS.value: application.id})

        application_search = ApplicationSearch(
            id=application.id,
            created=datetime.now(),
            updated=datetime.now(),
            user_id=application.user_id,
            company_id=application.company_id,
            job_id=application.job_id,
            user=user,
            application=application,
            user_details=user_details,
            application_ats=application_ats,
            job=job,
        )
        self.algolia_applications.create_object(
            object_id=application.id, object_data=application_search.dict()
        )

    async def update_application(self, processed_message: ProcessedAsyncMessage):
        application = cast(Application, processed_message.data)
        original_data = ApplicationSearch(
            **self.algolia_applications.get_object(
                object_id=processed_message.object_id
            )
        )
        original_data.application = application
        original_data.updated = datetime.now()
        self.algolia_applications.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )

    async def delete_application(self, processed_message: ProcessedAsyncMessage):
        original_data = ApplicationSearch(
            **self.algolia_applications.get_object(
                object_id=processed_message.object_id
            )
        )
        original_data.is_deleted = True
        original_data.updated = datetime.now()
        self.algolia_applications.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )

    async def update_application_ats(self, processed_message: ProcessedAsyncMessage):
        application_ats = cast(ATSDetails, processed_message.data)
        original_data = ApplicationSearch(
            **self.algolia_applications.get_object(
                object_id=processed_message.object_id
            )
        )
        original_data.application_ats = application_ats
        original_data.updated = datetime.now()
        self.algolia_applications.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )
