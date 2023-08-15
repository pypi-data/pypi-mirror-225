import typing as t
from influxdb_client_3 import InfluxDBClient3


class MockInfluxClient(InfluxDBClient3):
    def __init__(self, *args, **kwargs):
        self.local_items = []

    def query(self, query: str, database: t.Any, language: str):
        return self.local_items

    def write(self, database: str, record: t.Any):
        self.local_items.append("Some Results")
