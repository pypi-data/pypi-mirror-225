import typing as t

from fastapi import HTTPException


NotFoundException = HTTPException(status_code=404, detail="Item not found")
AlreadyExistsException = HTTPException(status_code=409, detail="Item already exists")
InvalidWebhookException = HTTPException(status_code=401, detail="Invalid webhook event")
NoCompanyFoundException = HTTPException(
    status_code=401, detail="User is not associated with a company"
)
JobHasBeenFilledException = HTTPException(status_code=400, detail="Job has been filled")
UserAlreadyAppliedException = HTTPException(
    status_code=400, detail="User has already applied to this job"
)
UserAlreadyRecruiterException = HTTPException(
    status_code=400, detail="You already exist as a recruiter for a different company"
)
CompanyNameAlreadyTakenException = HTTPException(
    status_code=400, detail="Company name already taken"
)
EmailFailedToSendException = HTTPException(
    status_code=500, detail="Failed to send email"
)
UserIsNotAdminException = HTTPException(status_code=401, detail="User is not an admin")
UserAdminPermissionsNotHighEnoughException = HTTPException(
    status_code=401, detail="User admin permissions are not high enough"
)
UserIsNotRecruiterException = HTTPException(
    status_code=401, detail="User is not a recruiter"
)
UserRecruiterPermissionsNotHighEnoughException = HTTPException(
    status_code=401, detail="User recruiter permissions are not high enough"
)


class EntityNotFound(HTTPException):
    def __init__(self, entity_name: str, entity_id: t.Optional[str] = None):
        detail_string = entity_name
        if entity_id:
            detail_string += f" with id {entity_id}"
        detail_string += " not found"
        super().__init__(
            status_code=404,
            detail=detail_string,
        )


class MultipleEntitiesReturned(HTTPException):
    def __init__(self, entity_name: str, entity_id: t.Optional[str] = None):
        detail_string = entity_name
        if entity_id:
            detail_string += f" with id {entity_id}"
        detail_string += " has multiple entries"
        super().__init__(
            status_code=404,
            detail=detail_string,
        )


class KafkaEventTopicNotProvidedError(Exception):
    def __init__(self):
        super().__init__("Kafka event topic must be provided")


class MissingParentKeyError(Exception):
    def __init__(self, parent_key: str):
        super().__init__(f"Missing parent key: {parent_key}")


class EntityDoesNotMatchError(Exception):
    def __init__(self, entity_type: str):
        super().__init__(f"{entity_type} Does not match")


class InvalidTokenException(Exception):
    def __init__(self, message="Invalid token"):
        self.message = message
        super().__init__(self.message)


class ExpiredTokenException(Exception):
    def __init__(self, message="Expired token"):
        self.message = message
        super().__init__(self.message)


class QStashBadDelayRequest(Exception):
    def __init__(self):
        super().__init__(
            "If you provide a delay, you must provide a delay unit, vice versa"
        )
