from requests import Response

from .companies.models import ClerkCompany
from .users.models import ClerkUser
from .recruiter_invitation.models import (
    ClerkCompanyInvitation,
    ClerkCompanyMemberType,
    ClerkInvitationStatus,
)
from .recruiters.models import (
    ClerkCompanyMembership,
    CreateClerkCompanyMember,
    ClerkCompanyCreated,
)
from .client import ClerkClient

mock_clerk_user = ClerkUser(
    id="abc123",
    object="nice",
    created_at=123,
    primary_email_address_id="abc123",
    email_addresses=[],
    phone_numbers=[],
    first_name="John",
    last_name="Doe",
    gender="male",
    birthday="1990-01-01",
)
mock_clerk_company = ClerkCompany(
    id="abc123",
    object="nice",
    created_at=123,
    created_by="abc",
    name="Test Company",
    slug="test-company",
    updated_at=123,
)
mock_clerk_company_invitation = ClerkCompanyInvitation(
    id="abc123",
    object="nice",
    created_at=123,
    email_address="asc",
    organization_id="abc",
    role=ClerkCompanyMemberType.admin,
    status=ClerkInvitationStatus.pending,
    updated_at=123,
)
mock_clerk_company_membership = ClerkCompanyMembership(
    id="abc123",
    object="nice",
    created_at=123,
    organization=ClerkCompanyCreated(
        id="abc123",
        object="nice",
    ),
    role=ClerkCompanyMemberType.admin,
    updated_at=123,
    public_user_data=CreateClerkCompanyMember(user_id="abc"),
)


class MockClerkClient(ClerkClient):
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        ...

    def _make_request(self, *args, **kwargs):
        resp = Response()
        resp.status_code = 200
        resp.json = lambda: kwargs["json"]  # type: ignore
        return resp

    def get_user(self, *args, **kwargs):
        return self._make_request(json=mock_clerk_user.dict())

    def get_company(self, company_id: str):
        return self._make_request(json=mock_clerk_company.dict())

    def get_company_invitations(self, company_id: str):
        return self._make_request(json=[mock_clerk_company_invitation.dict()])

    def get_company_recruiters(self, company_id):
        return self._make_request(json=[mock_clerk_company_membership.dict()])

    def get_companies_by_user_id(self, user_id):
        return self._make_request(json=[mock_clerk_company_membership.dict()])

    def get_all_users(self):
        return self._make_request(json=[mock_clerk_user.dict()])

    def get_all_companies(self):
        return self._make_request(json=[mock_clerk_company.dict()])
