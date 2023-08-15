from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import (
    KafkaEventConfig,
    KafkaTopic,
    KafkaUsersDetailsEnum,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection

from .models import UserDetails


class UserDetailsRepository(SingleChildRepository[UserDetails]):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
        kafka: KafkaProducerRepository | None,
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.users, message_type_enum=KafkaUsersDetailsEnum
        )
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.USER_DETAILS.value,
                entity_model=UserDetails,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
            ),
            required_parent_keys=[Entity.USERS.value],
        )
