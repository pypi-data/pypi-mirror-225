import openai


class MockOpenAI(openai.ChatCompletion):
    # pylint: disable=super-init-not-called
    # pylint: disable=abstract-method
    def __init__(self, *args, **kwargs):
        ...

    def create(self, *args, **kwargs):  # pylint: disable=arguments-differ
        return {
            "choices": [{"message": {"content": "Nice content"}}],
            "created": 1619798989,
            "id": "cmpl-2ZQ8Z9Z1X9X9Z",
            "model": "davinci:2020-05-03",
            "object": "text_completion",
        }
