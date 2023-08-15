import openai
from getajob.abstractions.vendor_client_factory import VendorClientFactory

from .mock import MockOpenAI
from .settings import OpenAIAPISettings


class OpenAIClientFactory(VendorClientFactory):
    @staticmethod
    def _return_mock():
        return MockOpenAI

    @staticmethod
    def _return_client():
        settings = OpenAIAPISettings()
        openai.api_key = settings.OPENAI_API_KEY
        return openai.ChatCompletion
