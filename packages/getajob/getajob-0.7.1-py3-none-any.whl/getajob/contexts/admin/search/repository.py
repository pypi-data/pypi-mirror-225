from getajob.abstractions.repository import query_subcollection
from getajob.abstractions.models import UserAndDatabaseConnection

from .models import AdminEntitySearch


class AdminSearchRepository:
    def __init__(self, request_scope: UserAndDatabaseConnection):
        self.db = request_scope.db

    def admin_search(self, search: AdminEntitySearch):
        return query_subcollection(db=self.db, collection_name=search.entity_type.value)
