from getajob.vendor.kafka.models import KafkaTopic

from .client import QStashClient
from .client_factory import QStashClientFactory
from .models import QStashDelay


class QStashRepository:
    def __init__(self, client: QStashClient = QStashClientFactory.get_client()):
        self.client = client

    def send_message(
        self,
        data: dict,
        kafka_topic: KafkaTopic,
        delay: int | None = None,
        delay_unit: QStashDelay | None = None,
    ):
        return self.client.send_message(
            data=data, kafka_topic=kafka_topic, delay=delay, delay_unit=delay_unit
        )
