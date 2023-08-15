from kafka import KafkaProducer, KafkaConsumer

from getajob.abstractions.vendor_client_factory import VendorClientFactory
from getajob.config.settings import SETTINGS

from .mock import MockKafkaProducer, MockKafkaConsumer
from .models import KafkaTopic, KafkaGroup


class KafkaProducerFactory(VendorClientFactory):
    @staticmethod
    def _return_mock():
        return MockKafkaProducer()

    @staticmethod
    def _return_client():
        return KafkaProducer(
            bootstrap_servers=[SETTINGS.KAFKA_BOOTSTRAP_SERVER],
            sasl_mechanism="SCRAM-SHA-256",
            security_protocol="SASL_SSL",
            sasl_plain_username=SETTINGS.KAFKA_USERNAME,
            sasl_plain_password=SETTINGS.KAFKA_PASSWORD,
        )


class KafkaConsumerFactory(VendorClientFactory):
    def __init__(self, group_id: KafkaGroup):
        self.group_id = group_id

    @staticmethod
    def _return_mock():
        return MockKafkaConsumer()

    # pylint: disable=arguments-differ
    @staticmethod
    def _return_client(group_id: KafkaGroup):  # type: ignore
        consumer = KafkaConsumer(
            bootstrap_servers=[SETTINGS.KAFKA_BOOTSTRAP_SERVER],
            sasl_mechanism="SCRAM-SHA-256",
            security_protocol="SASL_SSL",
            sasl_plain_username=SETTINGS.KAFKA_USERNAME,
            sasl_plain_password=SETTINGS.KAFKA_PASSWORD,
            auto_offset_reset="earliest",
            group_id=group_id.value,
        )
        consumer.subscribe(KafkaTopic.get_all_topics())
        return consumer

    # pylint: disable=arguments-differ
    def get_client(self):
        if SETTINGS.LOCAL_TESTING:
            return self._return_mock()
        return self._return_client(self.group_id)
