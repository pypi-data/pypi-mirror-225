from mockfirestore import MockFirestore


class MockFirestoreClient(MockFirestore):
    def close(self, *args, **kwargs):
        ...
