from getajob.abstractions.models import Entity
from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import UserAndDatabaseConnection

from .models import ChatMessage


class ChatMessageRepository(MultipleChildrenRepository[ChatMessage]):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.CHAT_MESSAGES.value,
                entity_model=ChatMessage,
            ),
            required_parent_keys=[Entity.CHAT.value],
        )
