from typing import Any, Type, Callable, Union, Dict
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class KafkaGroup(str, Enum):
    DATA_SERVICES = "data_services"
    NOTIFICATION_SERVICES = "notification_services"


class DataModelAndFunction(BaseModel):
    model: Type[BaseModel]
    function: Callable


class KafkaTopic(str, Enum):
    """Audit is not needed, it is assumed for all messages"""

    users = "users"
    jobs = "jobs"
    companies = "companies"
    applications = "applications"
    chat = "chat"
    api_logs = "api_logs"

    @classmethod
    def get_all_topics(cls):
        return [topic.value for topic in cls.__members__.values()]


class KafkaEventConfig(BaseModel):
    topic: KafkaTopic
    message_type_enum: Type[Enum]


class KafkaEventType(str, Enum):
    create = "create"
    update = "update"
    delete = "delete"
    get = "get"


class BaseKafkaMessage(BaseModel):
    object_id: str
    requesting_user_id: str
    parent_collections: dict[str, str] = {}
    message_type: str  # This is any of the enum values below, handled by consumer
    message_time: datetime = datetime.now()
    data: dict[str, Any] | None = None


class APILogMessage(BaseModel):
    status_code: int
    process_time: float
    company_id: str | None
    user_id: Union[str, int] = Field(default="anonymous")
    user_email: str = Field(default="anonymous")
    client_host: str = Field(default="unknown")
    method: str
    url: str
    query_params: Dict[str, Any]
    path_params: Dict[str, Any]
    message_time: datetime = datetime.now()

    def get_url_without_path_params(self):
        if not self.path_params:
            return self.url
        url = self.url
        for value in self.path_params.values():
            url = url.replace(f"/{value}", "")
        return url


class SearchImpressionData(BaseModel):
    index: str
    hits: list[str]  # The ids of the hits
    nbHits: int
    page: int
    query: str
    params: str
    search_time: datetime = datetime.now()


class KafkaAPILogsEnum(str, Enum):
    log = "log"


class KafkaUsersEnum(str, Enum):
    create = "create_user"
    update = "update_user"
    delete = "delete_user"


class KafkaUsersDetailsEnum(str, Enum):
    update = "update_user_details"
    get = "get_user_details"


class KafkaUserResumeExtraction(str, Enum):
    update = "update_user_resume_extraction"


class KafkaJobsEnum(str, Enum):
    create = "create_job"
    update = "update_job"
    delete = "delete_job"


class KafkaApplicationsEnum(str, Enum):
    create = "create_application"
    update = "update_application"
    delete = "delete_application"


class KafkaApplicationATSEnum(str, Enum):
    update = "update_ats"


class KafkaCompanyEnum(str, Enum):
    create = "create_company"
    update = "update_company"
    delete = "delete_company"


class KafkaCompanyDetailsEnum(str, Enum):
    update = "update_company_details"


class KafkaCandidatesEnum(str, Enum):
    create = "create_candidate"
    update = "update_candidate"


class KafkaChatEnum(str, Enum):
    create = "user_create_chat_message"


class KafkaAuditEnum(str, Enum):
    create = "create_audit"
