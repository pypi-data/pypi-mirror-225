import typing as t

from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import KafkaEventConfig, KafkaTopic, KafkaCompanyEnum
from getajob.abstractions.repository import ParentRepository, RepositoryDependencies
from getajob.abstractions.models import Entity, UserAndDatabaseConnection

from .models import (
    ClerkCompanyWebhookEvent,
    ClerkCompany,
    ClerkCompanyDeleted,
    ClerkCompanyWebhookType,
)
from .unit_of_work import ClerkCompanyUnitOfWork


class WebhookCompanyRepository(ParentRepository[ClerkCompany]):
    def __init__(
        self,
        request_scope: UserAndDatabaseConnection,
        kafka: t.Optional[KafkaProducerRepository] = None,
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.companies, message_type_enum=KafkaCompanyEnum
        )
        self.request_scope = request_scope
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.COMPANIES.value,
                entity_model=ClerkCompany,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
            )
        )

    def handle_webhook_event(self, event: ClerkCompanyWebhookEvent):
        event_dict = {
            ClerkCompanyWebhookType.organization_created: self.create_company,
            ClerkCompanyWebhookType.organization_updated: self.update_company,
            ClerkCompanyWebhookType.organization_deleted: self.delete_company,
        }
        return event_dict[event.type](event)

    def create_company(self, event: ClerkCompanyWebhookEvent):
        return ClerkCompanyUnitOfWork(
            request_scope=self.request_scope
        ).create_new_company(webhook_repository=self, event=event)

    def delete_company(self, event: ClerkCompanyWebhookEvent):
        delete_event = ClerkCompanyDeleted(**event.data)
        return self.delete(doc_id=delete_event.id)

    def update_company(self, event: ClerkCompanyWebhookEvent):
        update_event = ClerkCompany(**event.data)
        return self.update(doc_id=update_event.id, data=update_event)
