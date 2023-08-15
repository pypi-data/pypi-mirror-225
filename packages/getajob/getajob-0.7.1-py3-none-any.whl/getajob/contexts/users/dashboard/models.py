from pydantic import BaseModel


class UserDashboard(BaseModel):
    num_applications: int
    num_saved_jobs: int
