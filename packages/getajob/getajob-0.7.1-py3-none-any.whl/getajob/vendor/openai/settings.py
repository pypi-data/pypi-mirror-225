from pydantic import BaseModel
from getajob.utils import string_to_bool
from getajob.config.settings import SETTINGS


class OpenAIAPISettings(BaseModel):
    OPENAI_API_KEY: str = SETTINGS.OPENAI_API_KEY
    MOCK_RESPONSES: bool = string_to_bool(SETTINGS.OPENAI_API_KEY)
    MODEL_ABILITY: int = int(SETTINGS.OPENAI_MODEL_ABILITY)
    TEMPERATURE: float = 0.5
    TOP_P: float = 1.0
    FREQUENCY_PENALTY: float = 0.8
    PRESENCE_PENALTY: float = 0.0

    MODEL_ABILITY_DICT: dict = {1: "text-curie-001", 2: "gpt-3.5-turbo", 3: "gpt-4"}
    MODEL: str = "gpt-3.5-turbo"
