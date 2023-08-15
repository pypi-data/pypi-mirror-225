from getajob.vendor.clerk.companies.repository import WebhookCompanyRepository
from getajob.vendor.clerk.companies.models import ClerkCompanyWebhookEvent


class CompanyFixture:
    @staticmethod
    def create_company_from_webhook(request_scope):
        data = {
            "data": {
                "created_at": 1654013202977,
                "created_by": "user_1vq84bqWzw7qmFgqSwN4CH1Wp0n",
                "id": "org_29w9IfBrPmcpi0IeBVaKtA7R94W",
                "image_url": "https://img.clerk.com/xxxxxx",
                "logo_url": "https://example.org/example.png",
                "name": "Acme Inc",
                "object": "organization",
                "public_metadata": {},
                "slug": "acme-inc",
                "updated_at": 1654013202977,
            },
            "object": "event",
            "type": "organization.created",
        }
        company = ClerkCompanyWebhookEvent(**data)
        repo = WebhookCompanyRepository(request_scope)
        return repo.create_company(company)
