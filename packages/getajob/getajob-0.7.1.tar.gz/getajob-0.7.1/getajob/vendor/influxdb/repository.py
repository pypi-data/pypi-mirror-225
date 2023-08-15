"""
InfluxDB is used for search and analytics. It is a time series database.
Our use case is based on API Actions that occur in the system.

Examples of these actions are:
- User creates a job
- User creates a company
- User creates a job application
- Company Views an Application
- A job is recorded as a hit from a search event
- User views a job

Then we can build queries around this timeseries data to present analytics to the user.
"""
import typing as t
import json
from datetime import datetime
from influxdb_client_3 import InfluxDBClient3, Point

from .models import BucketAndMeasurement
from .client_factory import InfluxDBClientFactory


class InfluxDBSearchRepository:
    def __init__(
        self,
        bucket_and_database: BucketAndMeasurement,
        client: InfluxDBClient3 = InfluxDBClientFactory().get_client(),
    ):
        self.bucket_name = bucket_and_database.bucket
        self.measurement = bucket_and_database.measurement
        self.client = client

    def query(self, query: str, language: t.Literal["sql", "influxql"] = "sql"):
        """This query accepted SQL syntax"""
        return self.client.query(query, database=self.bucket_name, language=language)

    def write(self, data: dict, tags: list[str], time_field: str) -> None:
        """A tag is a field that is indexed so you can do fast filter operations on it."""
        point = Point(self.measurement)
        for tag in tags:
            point.tag(tag, data[tag])
        point.time(data[time_field])
        for key, value in data.items():
            if key not in tags and key != time_field:
                if isinstance(value, datetime):
                    value = value.isoformat()
                elif isinstance(value, dict):
                    value = json.dumps(value)
                point.field(key, value)
        self.client.write(database=self.bucket_name, record=point)
