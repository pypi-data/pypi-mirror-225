from getajob.exceptions import EntityDoesNotMatchError
from getajob.abstractions.models import Entity
from getajob.abstractions.repository import ParentRepository
from getajob.contexts.applications.repository import ApplicationRepository
from getajob.contexts.companies.recruiters.repository import RecruiterRepository
from getajob.contexts.users.repository import UserRepository

from .models import UserCreateChat


class CreateChatUnitOfWork:
    def __init__(
        self,
        application_repository: ApplicationRepository,
        recruiter_repository: RecruiterRepository,
        user_repository: UserRepository,
        chat_repository: ParentRepository,
    ):
        self.application_repository = application_repository
        self.recruiter_repository = recruiter_repository
        self.user_repository = user_repository
        self.chat_repository = chat_repository

    def create_new_chat(self, create_chat: UserCreateChat):
        # Verify that the application exists
        application = self.application_repository.get(create_chat.application_id)

        # Verify the application exists and matches the applicant
        applicant = self.user_repository.get(create_chat.applicant_user_id)
        if not application.user_id == applicant.id:
            raise EntityDoesNotMatchError("Applicant")

        # Verify that the recruiter exists under that given company
        assert self.recruiter_repository.get_one_by_attribute(
            "user_id",
            create_chat.recruiter_user_id,
            parent_collections={Entity.COMPANIES.value: create_chat.company_id},
        )

        # Create the chat
        return self.chat_repository.create(create_chat)
