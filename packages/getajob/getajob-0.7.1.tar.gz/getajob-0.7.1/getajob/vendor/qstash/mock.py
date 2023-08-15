class MockQStash:
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        self.messages_sent = 0

    def send_message(self, *args, **kwargs):
        self.messages_sent += 1
