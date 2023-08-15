import os
from datetime import datetime
from getajob.utils import replace_variables_in_html

from .client_factory import MailGunClientFactory, MailGunClient


class MailGunRepository:
    def __init__(
        self, mailgun_client: MailGunClient = MailGunClientFactory.get_client()
    ):
        self.client = mailgun_client
        self.absolute_path = os.path.dirname(os.path.abspath(__file__))

    def _send_email(self, to_address: str, subject: str, html_content: str):
        return self.client.send_email(to_address, subject, html_content)

    def send_chat_email(
        self,
        to_address: str,
        from_user_name: str,
        chat_message: str,
        chat_time: datetime,
    ):
        formatted_chat_time = chat_time.strftime("%B %d, %Y at %I:%M %p")
        with open(f"{self.absolute_path}/templates/chat_message.html", "r") as file:
            html_content = file.read()
        html_content = replace_variables_in_html(
            html_content,
            {
                "from": from_user_name,
                "message": chat_message,
                "message_time": formatted_chat_time,
            },
        )
        return self._send_email(to_address, "New Chat Message", html_content)
