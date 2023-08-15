from collections import defaultdict
from typing import Dict, List

from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection
from getajob.contexts.companies.jobs.repository import JobsRepository

from .models import SavedJob


class UserSavedJobsRepository(MultipleChildrenRepository[SavedJob]):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.USER_SAVED_JOBS.value,
                entity_model=SavedJob,
            ),
            required_parent_keys=[Entity.USERS.value],
        )
        self.request_scope = request_scope

    def _get_company_ids_and_job_ids(
        self, user_saved_jobs: list[SavedJob]
    ) -> Dict[str, List[str]]:
        company_ids = set()
        saved_company_jobs = defaultdict(list)
        for user_saved_job in user_saved_jobs:
            company_id = user_saved_job.company_id
            company_ids.add(company_id)
            saved_company_jobs[company_id].append(user_saved_job.job_id)
        return saved_company_jobs

    def _get_saved_jobs(
        self,
        user_saved_jobs: list[SavedJob],
        saved_company_jobs: Dict[str, List[str]],
        request_scope,
    ) -> list[SavedJob]:
        job_repo = JobsRepository(request_scope=request_scope, kafka=None)
        saved_jobs = []
        # TODO fix the get all by list function!!
        for company_id, job_ids in saved_company_jobs.items():
            company_jobs = job_repo.query(
                # items_to_get=job_ids,
                parent_collections={Entity.COMPANIES.value: company_id},
            ).data
            company_jobs_by_id = {job.id: job for job in company_jobs}
            for user_saved_job in user_saved_jobs:
                if user_saved_job.job_id in company_jobs_by_id:
                    saved_jobs.append(
                        SavedJob(
                            **user_saved_job.dict(exclude={"job"}),
                            job=company_jobs_by_id[user_saved_job.job_id]
                        )
                    )
        return saved_jobs

    def get_joined_user_saved_jobs(self, user_id: str) -> list[SavedJob]:
        user_saved_jobs = self.query(
            parent_collections={Entity.USERS.value: user_id}
        ).data
        saved_company_jobs = self._get_company_ids_and_job_ids(user_saved_jobs)
        return self._get_saved_jobs(
            user_saved_jobs, saved_company_jobs, self.request_scope
        )
