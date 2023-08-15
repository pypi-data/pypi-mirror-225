from getajob.abstractions.vendor_client_factory import VendorClientFactory

from .client import ClerkClient
from .mock import MockClerkClient


class ClerkClientFactory(VendorClientFactory):
    @staticmethod
    def _return_mock():
        return MockClerkClient()

    @staticmethod
    def _return_client():
        return ClerkClient()
