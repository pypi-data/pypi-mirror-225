from getajob.abstractions.models import UserAndDatabaseConnection, Entity
from getajob.vendor.kafka.models import (
    BaseKafkaMessage,
    KafkaJobsEnum,
    KafkaApplicationsEnum,
    KafkaCompanyDetailsEnum,
)

from .models import CreateAuditLog
from .repository import AuditLogRepository


class AsyncronousCompanyAuditService:
    def __init__(self, request_scope: UserAndDatabaseConnection):
        self.request_scope = request_scope

        self.audit_events = []
        self.audit_events.extend([v.value for v in KafkaApplicationsEnum])
        self.audit_events.extend([v.value for v in KafkaJobsEnum])
        self.audit_events.extend([v.value for v in KafkaCompanyDetailsEnum])

    async def _store_new_audit_record(self, new_log: CreateAuditLog):
        repo = AuditLogRepository(request_scope=self.request_scope)
        repo.create(
            new_log, parent_collections={Entity.COMPANIES.value: new_log.company_id}
        )

    def _convert_message_to_audit_record(
        self, message: BaseKafkaMessage
    ) -> CreateAuditLog | None:
        """Currently only auditing actions on jobs and applications"""
        if message.message_type not in self.audit_events:
            print(
                f"Message type: {message.message_type} not in audit events: {self.audit_events}"
            )
            return None
        if Entity.COMPANIES.value not in message.parent_collections:
            print(
                f"No company action taken with parent collections: {message.parent_collections}"
            )
            return None
        return CreateAuditLog(
            initiating_user_id=message.requesting_user_id,
            company_id=message.parent_collections[Entity.COMPANIES.value],
            action_type=message.message_type,
            action_time=message.message_time,
            action_data=message.data,
        )

    async def create_audit_record(self, message: BaseKafkaMessage):
        audit_record = self._convert_message_to_audit_record(message)
        if audit_record:
            await self._store_new_audit_record(audit_record)
