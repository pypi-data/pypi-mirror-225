from enum import Enum
from pydantic import BaseModel


class QStashDelay(str, Enum):
    seconds = "s"
    minutes = "m"
    hours = "h"
    days = "d"


class SendQStashMessage(BaseModel):
    data: dict
    jwt_token: str
