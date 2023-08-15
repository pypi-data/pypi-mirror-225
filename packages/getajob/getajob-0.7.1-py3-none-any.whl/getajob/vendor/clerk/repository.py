import typing
from requests import Response
from pydantic import BaseModel

from .companies.models import ClerkCompany
from .users.models import ClerkUser
from .recruiter_invitation.models import ClerkCompanyInvitation
from .recruiters.models import ClerkCompanyMembership

from .client import ClerkClient
from .client_factory import ClerkClientFactory


class ClerkAPIRepository:
    def __init__(self, client: ClerkClient = ClerkClientFactory.get_client()):  # type: ignore
        self.client = client

    def _format_response_to_model(
        self, response: Response, model: typing.Type[BaseModel]
    ):
        """
        Some clerk models return a 'data' key and others don't. This method
        formats the response to a pydantic model for both cases
        """
        response_json = response.json()
        if "data" in response_json:
            response_json = response_json["data"]
        if isinstance(response_json, list):
            return [model(**item) for item in response_json]
        return model(**response_json)

    def get_user(self, user_id: str):
        user = self.client.get_user(user_id)
        return self._format_response_to_model(user, ClerkUser)

    def get_company(self, company_id: str):
        company = self.client.get_company(company_id)
        return self._format_response_to_model(company, ClerkCompany)

    def get_company_invitations(self, company_id: str):
        invitations = self.client.get_company_invitations(company_id)
        return self._format_response_to_model(invitations, ClerkCompanyInvitation)

    def get_company_recruiters(self, company_id):
        recruiters = self.client.get_company_recruiters(company_id)
        return self._format_response_to_model(recruiters, ClerkCompanyMembership)

    def get_companies_by_user_id(self, user_id) -> typing.List[ClerkCompanyMembership]:
        companies = self.client.get_companies_by_user_id(user_id)
        return self._format_response_to_model(companies, ClerkCompanyMembership)  # type: ignore

    def get_all_users(self):
        users = self.client.get_all_users()
        return self._format_response_to_model(users, ClerkUser)

    def get_all_companies(self):
        companies = self.client.get_all_companies()
        return self._format_response_to_model(companies, ClerkCompany)
