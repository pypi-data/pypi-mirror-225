"""
This is an analytics repository meant to interact with influxdb
"""
import typing as t
from getajob.vendor.influxdb.repository import InfluxDBSearchRepository


class BaseAnalyticsRepository:
    def __init__(self, influx_db: InfluxDBSearchRepository):
        self.db = influx_db

    def query(self, query: str, language: t.Literal["sql", "influxql"] = "sql"):
        res = self.db.query(query, language)
        return res
