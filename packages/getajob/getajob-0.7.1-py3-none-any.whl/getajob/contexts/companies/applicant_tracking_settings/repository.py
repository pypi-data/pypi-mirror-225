from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection

from .models import ATSConfig


class CompanyATSConfigRepository(SingleChildRepository[ATSConfig]):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.COMPANY_ATS_CONFIG.value,
                entity_model=ATSConfig,
            ),
            required_parent_keys=[Entity.COMPANIES.value],
        )
