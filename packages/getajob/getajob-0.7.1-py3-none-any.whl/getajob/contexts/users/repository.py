from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import KafkaEventConfig, KafkaTopic, KafkaUsersEnum
from getajob.abstractions.repository import ParentRepository, RepositoryDependencies
from getajob.abstractions.models import Entity, UserAndDatabaseConnection
from .models import User


class UserRepository(ParentRepository[User]):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
        kafka: KafkaProducerRepository | None,
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.users, message_type_enum=KafkaUsersEnum
        )
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.USERS.value,
                entity_model=User,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
            )
        )

    def get_user(self, id: str):
        return super().get(id)

    @staticmethod
    def get_email_from_user(user: User):
        return [
            email
            for email in user.email_addresses
            if email.id == user.primary_email_address_id
        ][0].email_address
