from datetime import datetime, timedelta
import jwt

from getajob.exceptions import ExpiredTokenException, InvalidTokenException


def generate_jwt(
    username: str,
    jwt_secret: str,
    expire_datetime: datetime = (datetime.utcnow() + timedelta(seconds=60)),
):
    payload = {"iss": username, "iat": datetime.utcnow(), "exp": expire_datetime}
    return jwt.encode(payload, jwt_secret, algorithm="HS256")


def decode_jwt(token: str, kafka_jwt_secret: str):
    try:
        return jwt.decode(token, kafka_jwt_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()
    except jwt.InvalidTokenError:
        raise InvalidTokenException()
