from getajob.contexts.companies.jobs.repository import JobsRepository
from getajob.contexts.companies.jobs.models import UserCreateJob


class JobFixture:
    @staticmethod
    def create_job(request_scope, company_id: str):
        job = UserCreateJob(position_title="Software Engineer")
        repo = JobsRepository(request_scope=request_scope, kafka=None)
        return repo.create_job(company_id, job)
