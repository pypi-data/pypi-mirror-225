import requests

from getajob.abstractions.vendor_client_factory import VendorClientFactory
from getajob.config.settings import SETTINGS

from .mock import MockMailGunClient


class MailGunClient:
    def __init__(self):
        self.api_key = SETTINGS.MAILGUN_API_KEY
        self.base_api_url = SETTINGS.MAILGUN_BASE_API_URL
        self.from_email = SETTINGS.MAILGUN_FROM_EMAIL

    def send_email(self, to_email: str, subject: str, html_content: str):
        return requests.post(
            f"{self.base_api_url}/messages",
            auth=("api", self.api_key),
            data={
                "from": self.from_email,
                "to": to_email,
                "subject": subject,
                "text": html_content,
            },
            timeout=5,
        )


class MailGunClientFactory(VendorClientFactory):
    @staticmethod
    def _return_mock():
        return MockMailGunClient()

    @staticmethod
    def _return_client():
        return MailGunClient()
