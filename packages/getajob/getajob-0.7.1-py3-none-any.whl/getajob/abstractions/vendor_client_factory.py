from getajob.config.settings import SETTINGS


class VendorClientFactory:
    @staticmethod
    def _return_client():
        raise NotImplementedError()

    @staticmethod
    def _return_mock():
        raise NotImplementedError()

    @classmethod
    def get_client(cls):
        if SETTINGS.LOCAL_TESTING:
            return cls._return_mock()
        return cls._return_client()
