import os


def get_bool_from_string(string: str):
    return string.lower() in ("true", "1")


class AppSettings:
    # General
    APP_VERSION: str = os.getenv("APP_VERSION", "0.0.0")

    # Firebase config
    FIRESTORE_APP_NAME: str = "getajob"
    FIRESTORE_JSON_CONFIG: str = os.getenv("FIRESTORE_JSON_CONFIG", "")
    FIREBASE_FILE_STORAGE_BUCKET: str = os.getenv("FIREBASE_FILE_STORAGE_BUCKET", "")

    # Openai config
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MOCK_RESPONSES: str = os.getenv("OPENAI_MOCK_RESPONSES", "false")
    OPENAI_MODEL_ABILITY: int = 1

    # Clerk config
    CLERK_JWT_PEM_KEY: str = os.getenv("CLERK_JWT_PEM_KEY", "").replace(r"\n", "\n")
    CLERK_TOKEN_LEEWAY: int = int(os.getenv("CLERK_TOKEN_LEEWAY", "3600"))
    CLERK_USER_WEBHOOK_SECRET: str = os.getenv("CLERK_USER_WEBHOOK_SECRET", "")
    CLERK_SECRET_KEY: str = os.getenv("CLERK_SECRET_KEY", "")

    DEFAULT_PAGE_LIMIT: int = 20

    LOCAL_TESTING: bool = get_bool_from_string(os.getenv("LOCAL_TESTING", "false"))
    ENABLED_KAFKA_EVENTS: bool = get_bool_from_string(
        os.getenv("ENABLED_KAFKA_EVENTS", "false")
    )

    # Algolia config
    ALGOLA_APP_ID: str = os.getenv("ALGOLA_APP_ID", "")
    ALGOLIA_API_KEY: str = os.getenv("ALGOLIA_API_KEY", "")

    # Kafka config
    KAFKA_BOOTSTRAP_SERVER: str = os.getenv("KAFKA_BOOTSTRAP_SERVER", "")
    KAFKA_REST_URL: str = os.getenv("KAFKA_REST_URL", "")
    KAFKA_USERNAME: str = os.getenv("KAFKA_USERNAME", "")
    KAFKA_PASSWORD: str = os.getenv("KAFKA_PASSWORD", "")
    KAFKA_JWT_SECRET: str = os.getenv("KAFKA_JWT_SECRET", "")

    # Mailgun config
    MAILGUN_API_KEY: str = os.getenv("MAILGUN_API_KEY", "")
    MAILGUN_BASE_API_URL: str = os.getenv("MAILGUN_BASE_API_URL", "")
    MAILGUN_FROM_EMAIL: str = os.getenv("MAILGUN_FROM_EMAIL", "")

    # Sentry config
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    SENTRY_TRACES_RATE: float = 1.0

    # QStash config
    QSTASH_TOKEN: str = os.getenv("QSTASH_TOKEN", "")

    # InfluxDB config
    INFLUXDB_HOST: str = "https://us-east-1-1.aws.cloud2.influxdata.com"
    INFLUXDB_TOKEN: str = os.getenv("INFLUXDB_TOKEN", "")
    INFLUXDB_ORG: str = os.getenv("INFLUXDB_ORG", "")

    class Config:
        env_file = ".env"


SETTINGS = AppSettings()  # type: ignore
