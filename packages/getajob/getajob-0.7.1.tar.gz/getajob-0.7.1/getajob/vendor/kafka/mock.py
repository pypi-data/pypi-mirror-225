from kafka import KafkaProducer, KafkaConsumer


class MockKafkaProducer(KafkaProducer):
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        self.message_count = 0

    def send(self, *args, **kwargs):
        self.message_count += 1
        print("SENDING MESSAGE", args, kwargs)

    def flush(self, *args, **kwargs):
        ...

    def close(self, *args, **kwargs):
        ...


class MockKafkaConsumer(KafkaConsumer):
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        ...

    def poll(self, *args, **kwargs):
        ...

    def close(self, *args, **kwargs):
        ...

    def commit(self, *args, **kwargs):
        ...
