from datetime import datetime, timedelta

from getajob.contexts.scheduled_events.repository import ScheduledEventsRepository
from getajob.contexts.scheduled_events.models import (
    ScheduledEventCategory,
    CreateScheduledEvent,
)
from getajob.contexts.scheduled_events.enumerations import ReportScheduledEvent


class ScheduledEventsFixture:
    @staticmethod
    def create_scheduled_events(request_scope):
        event_1 = CreateScheduledEvent(
            related_object_id="test",
            name="Test Event",
            description="Test Description",
            cron="* * * * *",
            event_category=ScheduledEventCategory.REPORT,
            event_type=ReportScheduledEvent.APPLICANT_SUMMARY,
            next_run_time=datetime.utcnow() - timedelta(days=1),
        )
        event_2 = CreateScheduledEvent(
            related_object_id="test_2",
            name="Test Event 2",
            description="Test Description 2",
            cron="* * * * *",
            event_category=ScheduledEventCategory.REPORT,
            event_type=ReportScheduledEvent.APPLICANT_SUMMARY,
            next_run_time=datetime.utcnow() - timedelta(days=1),
        )
        event_3 = CreateScheduledEvent(
            related_object_id="test_3",
            name="Test Event 3",
            description="Test Description 3",
            cron="* * * * *",
            event_category=ScheduledEventCategory.REPORT,
            event_type=ReportScheduledEvent.APPLICANT_SUMMARY,
            next_run_time=datetime.utcnow() + timedelta(days=1),
        )
        repo = ScheduledEventsRepository(request_scope=request_scope)
        repo.create(event_1)
        repo.create(event_2)
        repo.create(event_3)
