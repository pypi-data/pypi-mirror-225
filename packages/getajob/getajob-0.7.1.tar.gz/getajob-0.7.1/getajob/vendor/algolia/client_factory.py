from algoliasearch.search_client import SearchClient
from getajob.abstractions.vendor_client_factory import VendorClientFactory
from getajob.config.settings import SETTINGS

from .mock import MockAlgoliaClient


class AlgoliaClientFactory(VendorClientFactory):
    @staticmethod
    def _return_mock():
        return MockAlgoliaClient()

    @staticmethod
    def _return_client():
        return SearchClient.create(SETTINGS.ALGOLA_APP_ID, SETTINGS.ALGOLIA_API_KEY)
