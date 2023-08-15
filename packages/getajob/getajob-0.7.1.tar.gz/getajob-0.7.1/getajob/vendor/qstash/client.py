from requests import request
from getajob.vendor.jwt import generate_jwt
from getajob.config.settings import SETTINGS
from getajob.exceptions import QStashBadDelayRequest
from getajob.vendor.kafka.models import KafkaTopic

from .models import QStashDelay, SendQStashMessage


class QStashClient:
    def __init__(self):
        self.token = SETTINGS.QSTASH_TOKEN
        self.base_url = "https://qstash.upstash.io/v1/publish"
        self.kafka_url = SETTINGS.KAFKA_REST_URL
        self.kafka_username = SETTINGS.KAFKA_USERNAME
        self.kafka_password = SETTINGS.KAFKA_PASSWORD

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _create_url(self, kafka_topic: KafkaTopic):
        return (
            f"{self.base_url}/{self.kafka_url}/webhook"
            f"?topic={kafka_topic.value}&user={self.kafka_username}&pass={self.kafka_password}"
        )

    def _send_request_to_kafka(
        self, url: str, message: SendQStashMessage, delay_header: dict | None
    ):
        if delay_header:
            headers = {**self._headers(), **delay_header}
        else:
            headers = self._headers()
        return request("POST", url, headers=headers, json=message.dict(), timeout=5)

    def _get_delay_header(self, delay: int | None, delay_unit: QStashDelay | None):
        if delay and not delay_unit or delay_unit and not delay:
            raise QStashBadDelayRequest()
        return {
            "Upstash-Delay": f"{delay}{delay_unit.value}"
            if delay and delay_unit
            else None
        }

    def send_message(
        self,
        data: dict,
        kafka_topic: KafkaTopic,
        delay: int | None = None,
        delay_unit: QStashDelay | None = None,
    ):
        return self._send_request_to_kafka(
            url=self._create_url(kafka_topic),
            delay_header=self._get_delay_header(delay, delay_unit),
            message=SendQStashMessage(
                data=data,
                jwt_token=generate_jwt(
                    SETTINGS.KAFKA_USERNAME, SETTINGS.KAFKA_JWT_SECRET
                ),
            ),
        )
