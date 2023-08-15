from typing import cast
from datetime import datetime

from getajob.abstractions.models import Entity, ProcessedAsyncMessage
from getajob.vendor.algolia.repository import AlgoliaSearchRepository
from getajob.contexts.search.models import CompanySearch

from .models import Company
from .details.models import CompanyDetails


class AsyncronousCompanyService:
    def __init__(self, algolia_companies: AlgoliaSearchRepository):
        self.algolia_companies = algolia_companies

    async def company_is_created(self, processed_message: ProcessedAsyncMessage):
        data = cast(Company, processed_message.data)
        company_data = CompanySearch(
            company=data,
            id=data.id,
            created=datetime.now(),
            updated=datetime.now(),
        )
        self.algolia_companies.create_object(
            object_id=data.id, object_data=company_data.dict()
        )

    async def company_is_updated(self, processed_message: ProcessedAsyncMessage):
        data = cast(Company, processed_message.data)
        original_data = CompanySearch(
            **self.algolia_companies.get_object(object_id=data.id)
        )
        original_data.company = data
        original_data.updated = datetime.now()
        self.algolia_companies.update_object(
            object_id=data.id, object_data=original_data.dict()
        )

    async def company_is_deleted(self, processed_message: ProcessedAsyncMessage):
        original_data = CompanySearch(
            **self.algolia_companies.get_object(object_id=processed_message.object_id)
        )
        original_data.is_deleted = True
        original_data.updated = datetime.now()
        self.algolia_companies.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )

    async def company_details_are_set(self, processed_message: ProcessedAsyncMessage):
        data = cast(CompanyDetails, processed_message.data)
        original_data = CompanySearch(
            **self.algolia_companies.get_object(
                object_id=processed_message.parent_collections[Entity.COMPANIES.value]
            )
        )
        original_data.company_details = data
        original_data.updated = datetime.now()
        self.algolia_companies.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )
