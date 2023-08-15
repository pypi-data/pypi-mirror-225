from getajob.abstractions.models import Entity
from getajob.abstractions.repository import ParentRepository, RepositoryDependencies
from getajob.vendor.firestore.models import FirestoreFilters
from getajob.abstractions.models import UserAndDatabaseConnection
from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import (
    KafkaEventConfig,
    KafkaTopic,
    KafkaApplicationsEnum,
)
from getajob.contexts.users.resumes.repository import ResumeRepository
from getajob.contexts.companies.jobs.repository import JobsRepository
from getajob.contexts.applications.applicant_tracking.repository import ATSRepository

from .models import UserCreatedApplication, Application
from .unit_of_work import ApplicationsUnitOfWork


class ApplicationRepository(ParentRepository[Application]):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
        kafka: KafkaProducerRepository | None,
    ):
        self.request_scope = request_scope
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.applications, message_type_enum=KafkaApplicationsEnum
        )
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.APPLICATIONS.value,
                entity_model=Application,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
            ),
        )

    def user_creates_application(
        self, user_id: str, application: UserCreatedApplication
    ):
        return ApplicationsUnitOfWork(self).user_creates_application(
            user_id=user_id,
            resume_repo=ResumeRepository(request_scope=self.request_scope),
            job_repo=JobsRepository(request_scope=self.request_scope, kafka=None),
            applicant_tracking_repo=ATSRepository(
                request_scope=self.request_scope, kafka=None
            ),
            create_application=application,
        )

    def get_applications_by_company(self, company_id: str):
        return super().query(
            filters=[
                FirestoreFilters(field="company_id", operator="==", value=company_id),
            ],
        )

    def get_applications_by_job(self, company_id: str, job_id: str):
        return super().query(
            filters=[
                FirestoreFilters(field="company_id", operator="==", value=company_id),
                FirestoreFilters(field="job_id", operator="==", value=job_id),
            ],
        )

    def get_application_by_job_and_application_id(
        self, company_id: str, job_id: str, job_application_id: str
    ):
        return super().get_with_filters(
            doc_id=job_application_id,
            filters=[
                FirestoreFilters(field="company_id", operator="==", value=company_id),
                FirestoreFilters(field="job_id", operator="==", value=job_id),
            ],
        )

    def get_applications_by_user(self, user_id):
        return super().query(
            filters=[
                FirestoreFilters(
                    field="user_id",
                    operator="==",
                    value=user_id,
                )
            ],
        )

    def get_application_by_user_id_and_application_id(
        self, user_id: str, job_application_id: str
    ):
        return super().get_with_filters(
            doc_id=job_application_id,
            filters=[
                FirestoreFilters(
                    field="user_id",
                    operator="==",
                    value=user_id,
                )
            ],
        )
