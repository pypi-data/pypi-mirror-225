from typing import cast
from datetime import datetime

from getajob.abstractions.models import (
    Entity,
    ProcessedAsyncMessage,
    UserAndDatabaseConnection,
)
from getajob.vendor.firestore.models import FirestoreFilters
from getajob.vendor.algolia.repository import AlgoliaSearchRepository
from getajob.contexts.search.models import CandidateSearch
from getajob.contexts.applications.repository import ApplicationRepository

from .models import User
from .details.models import UserDetails


class AsyncronousUserService:
    def __init__(
        self,
        algolia_users: AlgoliaSearchRepository,
        algolia_applications: AlgoliaSearchRepository,
    ):
        self.algolia_users = algolia_users
        self.algolia_applications = algolia_applications

    async def user_is_created(self, processed_message: ProcessedAsyncMessage):
        data = cast(User, processed_message.data)
        candidate_data = CandidateSearch(
            user=data,
            id=data.id,
            created=datetime.now(),
            updated=datetime.now(),
            thumbnail=data.image_url,
        )
        self.algolia_users.create_object(
            object_id=data.id, object_data=candidate_data.dict()
        )

    def _get_all_user_application_ids(
        self, request_scope: UserAndDatabaseConnection, user_id: str
    ):
        all_user_applications = ApplicationRepository(
            request_scope=request_scope, kafka=None
        ).query(
            filters=[
                FirestoreFilters(
                    field="user_id",
                    operator="==",
                    value=user_id,
                )
            ]
        )
        return [application.id for application in all_user_applications.data]

    async def _update_all_user_in_applications(
        self, request_scope: UserAndDatabaseConnection, user_id: str, new_user: User
    ):
        objects_to_update = [
            {
                "objectID": app_id,
                "user": new_user.dict(),
                "updated": datetime.now(),
            }
            for app_id in self._get_all_user_application_ids(request_scope, user_id)
        ]
        self.algolia_applications.partial_update_based_on_attribute(objects_to_update)

    async def _update_all_user_details_in_applications(
        self,
        request_scope: UserAndDatabaseConnection,
        user_id: str,
        new_user_details: UserDetails,
    ):
        objects_to_update = [
            {
                "objectID": app_id,
                "user_details": new_user_details.dict(),
                "updated": datetime.now(),
            }
            for app_id in self._get_all_user_application_ids(request_scope, user_id)
        ]
        self.algolia_applications.partial_update_based_on_attribute(objects_to_update)

    async def _delete_all_user_applications(
        self, request_scope: UserAndDatabaseConnection, user_id: str
    ):
        objects_to_update = [
            {
                "objectID": app_id,
                "user_is_deleted": True,
                "updated": datetime.now(),
            }
            for app_id in self._get_all_user_application_ids(request_scope, user_id)
        ]
        self.algolia_applications.partial_update_based_on_attribute(objects_to_update)

    async def user_is_updated(self, processed_message: ProcessedAsyncMessage):
        data = cast(User, processed_message.data)
        original_data = CandidateSearch(
            **self.algolia_users.get_object(object_id=data.id)
        )
        original_data.user = data
        original_data.updated = datetime.now()
        original_data.thumbnail = data.image_url
        self.algolia_users.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )
        await self._update_all_user_in_applications(
            processed_message.request_scope, data.id, data
        )

    async def user_is_deleted(self, processed_message: ProcessedAsyncMessage):
        original_data = CandidateSearch(
            **self.algolia_users.get_object(object_id=processed_message.object_id)
        )
        original_data.is_deleted = True
        original_data.updated = datetime.now()
        self.algolia_users.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )
        await self._delete_all_user_applications(
            processed_message.request_scope, processed_message.object_id
        )

    async def user_details_are_created_or_updated(
        self, processed_message: ProcessedAsyncMessage
    ):
        user_id = processed_message.parent_collections[Entity.USERS.value]
        data = cast(UserDetails, processed_message.data)
        original_data = CandidateSearch(
            **self.algolia_users.get_object(object_id=user_id)
        )
        original_data.user_details = data
        original_data.updated = datetime.now()
        self.algolia_users.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )
        await self._update_all_user_details_in_applications(
            processed_message.request_scope, user_id, data
        )
