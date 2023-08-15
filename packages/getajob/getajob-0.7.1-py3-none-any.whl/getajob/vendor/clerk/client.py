from fastapi import HTTPException
from requests import request, Response

from getajob.config.settings import SETTINGS
from getajob.exceptions import EntityNotFound


class ClerkClient:
    def __init__(self):
        self.api_key = SETTINGS.CLERK_SECRET_KEY
        self.base_url = "https://api.clerk.dev"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _make_request(
        self, method: str, endpoint: str, payload: dict | None = None
    ) -> Response:
        url = self.base_url + endpoint
        request_payload = {"method": method, "url": url, "headers": self._headers()}
        if payload:
            request_payload["json"] = payload
        response = request(**request_payload, timeout=10)
        if response.status_code == 404:
            raise EntityNotFound(endpoint)
        if response.status_code != 200:
            raise HTTPException(
                status_code=500, detail=f"Error: {response.status_code} {response.text}"
            )
        return response

    def get_user(self, user_id: str):
        endpoint = f"/v1/users/{user_id}"
        return self._make_request("GET", endpoint)

    def get_company(self, company_id: str):
        endpoint = f"/v1/organizations/{company_id}"
        return self._make_request("GET", endpoint)

    def get_company_invitations(self, company_id: str):
        endpoint = f"/v1/organizations/{company_id}/invitations/pending"
        return self._make_request("GET", endpoint)

    def get_company_recruiters(self, company_id):
        endpoint = f"/v1/organizations/{company_id}/memberships"
        return self._make_request("GET", endpoint)

    def get_companies_by_user_id(self, user_id):
        endpoint = f"/v1/users/{user_id}/organization_memberships"
        return self._make_request("GET", endpoint)

    def get_all_users(self):
        endpoint = "/v1/users"
        return self._make_request("GET", endpoint)

    def get_all_companies(self):
        endpoint = "/v1/organizations"
        return self._make_request("GET", endpoint)
