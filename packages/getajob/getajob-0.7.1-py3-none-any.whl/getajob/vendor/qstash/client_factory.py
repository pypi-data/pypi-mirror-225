from getajob.abstractions.vendor_client_factory import VendorClientFactory

from .mock import MockQStash
from .client import QStashClient


class QStashClientFactory(VendorClientFactory):
    @staticmethod
    def _return_mock():
        return MockQStash()

    @staticmethod
    def _return_client():
        return QStashClient()
