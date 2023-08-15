from enum import Enum
from datetime import datetime
from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class ResultEnum(str, Enum):
    success = "success"
    failure = "failure"


class CreateAuditLog(BaseModel):
    initiating_user_id: str
    company_id: str
    action_type: str
    action_time: datetime
    action_data: dict | None
    with_result: ResultEnum = ResultEnum.success


class AuditLog(CreateAuditLog, BaseDataModel):
    ...
