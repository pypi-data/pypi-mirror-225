from datetime import datetime

from getajob.exceptions import NotFoundException
from getajob.abstractions.repository import MultipleChildrenRepository
from getajob.abstractions.models import Entity
from getajob.vendor.firebase_storage.repository import FirebaseStorageRepository

from .models import Resume, CreateResume, UserCreateResume


class ResumeUnitOfWork:
    def __init__(
        self,
        resume_repo: MultipleChildrenRepository,
        storage_repo: FirebaseStorageRepository,
    ):
        self.resume_repo = resume_repo
        self.storage_repo = storage_repo

    def _create_file_path(self, user_id: str):
        return f"{user_id}/resumes/{int(datetime.now().timestamp())}"

    def create_user_resume(self, user_id, data: UserCreateResume) -> Resume:
        # First upload the file then store the resulting URL in the resume record and save
        remote_file_path = self._create_file_path(user_id)
        resume_url = self.storage_repo.upload_bytes(
            data.resume_data, data.file_type, remote_file_path, True
        )
        return self.resume_repo.create(
            CreateResume(
                resume_url=resume_url,
                remote_file_path=remote_file_path,
                **data.dict(),
            ),
            parent_collections={Entity.USERS.value: user_id},
        )

    def delete_user_resume(self, user_id: str, resume_id: str):
        # Get the resume from database
        resume = self.resume_repo.get(
            resume_id, parent_collections={Entity.USERS.value: user_id}
        )
        if not resume:
            return None

        # Delete the file from storage
        self.storage_repo.delete_file(resume.remote_file_path)

        # Delete the resume from database
        self.resume_repo.delete(
            resume_id, parent_collections={Entity.USERS.value: user_id}
        )

    def update_user_resume(
        self, user_id, resume_id: str, data: UserCreateResume
    ) -> Resume:
        # Get the resume from database
        resume = self.resume_repo.get(
            resume_id, parent_collections={Entity.USERS.value: user_id}
        )
        if not resume:
            raise NotFoundException

        # Update the file in storage
        self.storage_repo.upload_bytes(
            data.resume_data, data.file_type, resume.remote_file_path, True
        )
        return self.resume_repo.update(
            resume_id,
            CreateResume(
                resume_url=resume.resume_url, remote_file_path=resume.remote_file_path
            ),
            parent_collections={Entity.USERS.value: user_id},
        )
