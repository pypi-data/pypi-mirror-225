from pydantic import BaseModel


class AdminDashboard(BaseModel):
    total_applications: int
    total_jobs: int
    total_companies: int
    total_users: int
