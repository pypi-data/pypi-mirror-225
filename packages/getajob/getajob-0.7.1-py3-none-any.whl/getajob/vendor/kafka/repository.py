import json
from kafka import KafkaProducer, KafkaConsumer

from getajob.vendor.kafka.models import (
    KafkaTopic,
    BaseKafkaMessage,
    APILogMessage,
    SearchImpressionData,
)
from getajob.config.settings import SETTINGS
from getajob.vendor.jwt import generate_jwt

from .client_factory import KafkaProducerFactory


class KafkaProducerRepository:
    def __init__(self, producer: KafkaProducer = KafkaProducerFactory.get_client()):  # type: ignore
        # The client provides a producer that is already connected
        self.producer = producer

    # TASK this message paramter is now gross
    def publish(
        self,
        topic: KafkaTopic,
        message: BaseKafkaMessage | APILogMessage | SearchImpressionData,
    ) -> None:
        message_token = generate_jwt(SETTINGS.KAFKA_USERNAME, SETTINGS.KAFKA_JWT_SECRET)
        self.producer.send(
            topic.value,
            json.dumps(message.dict(), default=str).encode("utf-8"),
            headers=[("authorization", message_token.encode("utf-8"))],
        )

    def disconnect(self):
        self.producer.flush()
        self.producer.close()


class KafkaConsumerRepository:
    def __init__(self, consumer: KafkaConsumer):
        self.consumer = consumer

    def poll(
        self, timeout: int = 100, max_records: int = 20, update_offsets: bool = True
    ) -> None:
        self.consumer.poll(timeout, max_records, update_offsets)

    def disconnect(self) -> None:
        self.consumer.close()
