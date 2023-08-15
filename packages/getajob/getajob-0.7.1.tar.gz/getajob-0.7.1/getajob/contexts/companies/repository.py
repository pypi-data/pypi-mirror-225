from getajob.vendor.firestore.models import FirestoreFilters
from getajob.abstractions.repository import ParentRepository, RepositoryDependencies
from getajob.abstractions.models import Entity, UserAndDatabaseConnection
from getajob.vendor.kafka.models import KafkaEventConfig, KafkaTopic, KafkaCompanyEnum
from getajob.vendor.kafka.repository import KafkaProducerRepository

from .models import Company


class CompanyRepository(ParentRepository[Company]):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
        kafka: KafkaProducerRepository | None,
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.companies, message_type_enum=KafkaCompanyEnum
        )
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.COMPANIES.value,
                entity_model=Company,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
            )
        )

    def get_companies_by_company_id_list(self, company_id_list: list[str]):
        return self.query(
            filters=[FirestoreFilters(field="id", operator="in", value=company_id_list)]
        )
