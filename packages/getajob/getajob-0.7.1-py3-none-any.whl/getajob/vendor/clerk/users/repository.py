import typing as t

from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import KafkaEventConfig, KafkaTopic, KafkaUsersEnum
from getajob.abstractions.repository import ParentRepository, RepositoryDependencies
from getajob.abstractions.models import Entity, UserAndDatabaseConnection
from getajob.contexts.users.details.repository import UserDetailsRepository
from getajob.contexts.users.details.models import SetUserDetails

from .models import (
    ClerkUser,
    ClerkUserWebhookEvent,
    ClerkUserWebhookType,
    ClerkWebhookUserDeleted,
    ClerkWebhookUserUpdated,
)


class WebhookUserRepository(ParentRepository[ClerkUser]):
    def __init__(
        self,
        request_scope: UserAndDatabaseConnection,
        kafka: t.Optional[KafkaProducerRepository] = None,
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.users, message_type_enum=KafkaUsersEnum
        )
        self.request_scope = request_scope
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.USERS.value,
                entity_model=ClerkUser,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
            )
        )

    def handle_webhook_event(self, event: ClerkUserWebhookEvent):
        event_dict = {
            ClerkUserWebhookType.user_created: self.create_user,
            ClerkUserWebhookType.user_updated: self.update_user,
            ClerkUserWebhookType.user_deleted: self.delete_user,
        }
        return event_dict[event.type](event)

    def _create_default_user_details(self, user_id: str):
        UserDetailsRepository(
            request_scope=self.request_scope, kafka=None
        ).set_sub_entity(
            data=SetUserDetails(),
            parent_collections={Entity.USERS.value: user_id},
        )

    def create_user(self, event: ClerkUserWebhookEvent):
        create_event = ClerkUser(**event.data)
        res = self.create(data=create_event, provided_id=create_event.id)
        self._create_default_user_details(user_id=create_event.id)
        return res

    def update_user(self, event: ClerkUserWebhookEvent):
        update_event = ClerkWebhookUserUpdated(**event.data)
        return self.update(doc_id=update_event.id, data=update_event)

    def delete_user(self, event: ClerkUserWebhookEvent):
        delete_event = ClerkWebhookUserDeleted(**event.data)
        return self.delete(doc_id=delete_event.id)
