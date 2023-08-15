from typing import cast

from getajob.abstractions.models import UserAndDatabaseConnection, ProcessedAsyncMessage
from getajob.contexts.users.repository import UserRepository
from getajob.contexts.chat.repository import ChatRepository
from getajob.contexts.chat.message.models import KafkaChatMessage
from getajob.vendor.mailgun.repository import MailGunRepository


class AsyncronousChatService:
    def __init__(self, mailgun: MailGunRepository):
        self.mailgun = mailgun

    async def _get_chat(self, chat_id: str, request_scope: UserAndDatabaseConnection):
        return ChatRepository(request_scope=request_scope).get(chat_id)

    async def send_chat_message_as_email(
        self, processed_message: ProcessedAsyncMessage
    ):
        user_repo = UserRepository(
            request_scope=processed_message.request_scope, kafka=None
        )
        new_message = cast(KafkaChatMessage, processed_message.data)

        chat = await self._get_chat(
            new_message.chat_id,
            processed_message.request_scope,
        )
        if processed_message.request_scope.initiating_user_id == chat.recruiter_user_id:
            # Send to applicant
            email_receiving_user = user_repo.get(chat.applicant_user_id)
            email_sending_user = user_repo.get(chat.recruiter_user_id)
        else:
            # Send to recruiter
            email_receiving_user = user_repo.get(chat.recruiter_user_id)
            email_sending_user = user_repo.get(chat.applicant_user_id)

        receiving_user_email_address = user_repo.get_email_from_user(
            email_receiving_user
        )
        print(
            f"Sending Email to {receiving_user_email_address} \
            from {email_sending_user.first_name} {email_sending_user.last_name} \
            with message {new_message.message} at {new_message.message_time} "
        )
        self.mailgun.send_chat_email(
            to_address=receiving_user_email_address,
            from_user_name=email_sending_user.first_name,
            chat_message=new_message.message,
            chat_time=new_message.message_time,
        )
