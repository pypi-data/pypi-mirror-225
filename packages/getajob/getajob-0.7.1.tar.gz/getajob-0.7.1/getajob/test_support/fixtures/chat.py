from getajob.contexts.chat.repository import ChatRepository
from getajob.contexts.chat.models import UserCreateChat
from getajob.test_support.fixtures.application import ApplicationFixture
from getajob.test_support.fixtures.recruiter import RecruiterFixture

from .application import ApplicationFixture, ApplicationWithDependencies


class ChatWithDependencies(ApplicationWithDependencies):
    chat_id: str
    recruiter_id: str


class ChatFixture:
    @staticmethod
    def create_chat_with_dependencies(request_scope):
        application_and_dependencies = (
            ApplicationFixture.create_application_with_dependencies(request_scope)
        )
        recruiter = RecruiterFixture.create_recruiter_from_webhook(request_scope)
        repo = ChatRepository(request_scope=request_scope)
        new_chat = repo.create_new_chat(
            UserCreateChat(
                applicant_user_id=application_and_dependencies.application.user_id,
                recruiter_user_id=recruiter.user_id,
                application_id=application_and_dependencies.application.id,
                company_id=application_and_dependencies.company.id,
            )
        )
        return ChatWithDependencies(
            chat_id=new_chat.id,
            recruiter_id=recruiter.id,
            application=application_and_dependencies.application,
            company=application_and_dependencies.company,
            job=application_and_dependencies.job,
            resume=application_and_dependencies.resume,
            user=application_and_dependencies.user,
        )
