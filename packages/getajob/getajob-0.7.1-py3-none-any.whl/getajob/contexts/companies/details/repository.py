from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import (
    KafkaEventConfig,
    KafkaTopic,
    KafkaCompanyDetailsEnum,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection

from .models import CompanyDetails


class CompanyDetailsRepository(SingleChildRepository[CompanyDetails]):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
        kafka: KafkaProducerRepository | None,
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.companies, message_type_enum=KafkaCompanyDetailsEnum
        )
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.COMPANY_DETAILS.value,
                entity_model=CompanyDetails,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
            ),
            required_parent_keys=[Entity.COMPANIES.value],
        )
