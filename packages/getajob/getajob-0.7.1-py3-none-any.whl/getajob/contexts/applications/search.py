"""
Search from algolia
"""

from getajob.vendor.algolia.repository import AlgoliaSearchRepository
from getajob.vendor.algolia.models import AlgoliaSearchParams, AlgoliaSearchResults

from .models import (
    CompanyQueryApplications,
    UserQueryApplications,
)


class ApplicationSearchRepository:
    def __init__(self, algolia_applications: AlgoliaSearchRepository):
        self.algolia_applications = algolia_applications
