from typing import cast
from datetime import datetime

from getajob.abstractions.models import (
    Entity,
    ProcessedAsyncMessage,
    UserAndDatabaseConnection,
)
from getajob.vendor.firestore.models import FirestoreFilters
from getajob.vendor.algolia.repository import AlgoliaSearchRepository
from getajob.contexts.search.models import JobSearch
from getajob.contexts.applications.repository import ApplicationRepository

from .models import Job


class AsyncronousJobService:
    def __init__(
        self,
        algolia_jobs: AlgoliaSearchRepository,
        algolia_applications: AlgoliaSearchRepository,
    ):
        self.algolia_jobs = algolia_jobs
        self.algolia_applications = algolia_applications

    async def create_job(self, processed_message: ProcessedAsyncMessage):
        job_data = cast(Job, processed_message.data)
        self.algolia_jobs.create_object(
            object_id=job_data.id,
            object_data=JobSearch(
                id=job_data.id,
                created=datetime.now(),
                updated=datetime.now(),
                job=job_data,
                company_id=processed_message.parent_collections[Entity.COMPANIES.value],
            ).dict(),
        )

    def _get_all_job_application_ids(
        self, request_scope: UserAndDatabaseConnection, job_id: str
    ):
        all_user_applications = ApplicationRepository(
            request_scope=request_scope, kafka=None
        ).query(
            filters=[
                FirestoreFilters(
                    field="job_id",
                    operator="==",
                    value=job_id,
                )
            ]
        )
        return [application.id for application in all_user_applications.data]

    async def _update_all_applications_with_job(
        self, request_scope: UserAndDatabaseConnection, job: Job
    ):
        objects_to_update = [
            {
                "objectID": app_id,
                "job": job.dict(),
                "updated": datetime.now(),
            }
            for app_id in self._get_all_job_application_ids(
                request_scope=request_scope, job_id=job.id
            )
        ]
        self.algolia_applications.partial_update_based_on_attribute(objects_to_update)

    async def _delete_all_applications_with_job(
        self, request_scope: UserAndDatabaseConnection, job_id: str
    ):
        objects_to_update = [
            {
                "objectID": app_id,
                "job_is_deleted": True,
                "updated": datetime.now(),
            }
            for app_id in self._get_all_job_application_ids(
                request_scope=request_scope, job_id=job_id
            )
        ]
        self.algolia_applications.partial_update_based_on_attribute(objects_to_update)

    async def _handle_job_is_now_filled(
        self, request_scope: UserAndDatabaseConnection, job_id: str
    ):
        objects_to_update = [
            {
                "objectID": app_id,
                "job_is_filled": True,
                "updated": datetime.now(),
            }
            for app_id in self._get_all_job_application_ids(
                request_scope=request_scope, job_id=job_id
            )
        ]
        self.algolia_applications.partial_update_based_on_attribute(objects_to_update)

    async def update_job(self, processed_message: ProcessedAsyncMessage):
        original_data = JobSearch(
            **self.algolia_jobs.get_object(object_id=processed_message.object_id)
        )
        job_updates = cast(Job, processed_message.data)
        if job_updates.position_filled:
            await self._handle_job_is_now_filled(
                processed_message.request_scope, original_data.id
            )
        original_data.job = job_updates
        original_data.updated = datetime.now()
        self.algolia_jobs.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )
        await self._update_all_applications_with_job(
            processed_message.request_scope, original_data.job
        )

    async def delete_job(self, processed_message: ProcessedAsyncMessage):
        original_data = JobSearch(
            **self.algolia_jobs.get_object(object_id=processed_message.object_id)
        )
        original_data.is_deleted = True
        original_data.updated = datetime.now()
        self.algolia_jobs.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )
        await self._delete_all_applications_with_job(
            processed_message.request_scope, original_data.id
        )
