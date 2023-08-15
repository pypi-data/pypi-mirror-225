class MockMailGunClient:
    def __init__(self):
        self.sent_emails = []

    def send_email(self, to_email: str, subject: str, html_content: str):
        self.sent_emails.append(
            {"to_email": to_email, "subject": subject, "html_content": html_content}
        )
