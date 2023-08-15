"""Single child repository under an application, only visibile to the company"""


from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import (
    KafkaEventConfig,
    KafkaTopic,
    KafkaApplicationATSEnum,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection

from .models import ATSDetails


class ATSRepository(SingleChildRepository[ATSDetails]):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
        kafka: KafkaProducerRepository | None,
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.applications, message_type_enum=KafkaApplicationATSEnum
        )
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.APPLICATION_TRACKING.value,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
                entity_model=ATSDetails,
            ),
            required_parent_keys=[Entity.APPLICATIONS.value],
        )
