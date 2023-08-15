from influxdb_client_3 import InfluxDBClient3, flight_client_options
import certifi

from getajob.abstractions.vendor_client_factory import VendorClientFactory
from getajob.config.settings import SETTINGS

from .mock import MockInfluxClient


class InfluxDBClientFactory(VendorClientFactory):
    @staticmethod
    def _return_mock():
        return MockInfluxClient()

    @staticmethod
    def _return_client():
        with open(certifi.where(), "r") as fh:
            cert = fh.read()
        return InfluxDBClient3(
            host=SETTINGS.INFLUXDB_HOST,
            token=SETTINGS.INFLUXDB_TOKEN,
            org=SETTINGS.INFLUXDB_ORG,
            flight_client_options=flight_client_options(tls_root_certs=cert),
        )
