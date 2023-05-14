from datetime import datetime, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from api.models import Case


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def clear_old_notes() -> None:
    """
    This job deletes all notes from cases that are older than 90 days.
    """
    try:
        old_cases = Case.objects.get(edited_at__lte=datetime.now() - timedelta(days=90))
    except Case.DoesNotExist:
        return

    for case in old_cases:
        case.notes = None
        case.save()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age: int = 604_800) -> None:
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    """
    Defines a management command that starts the APScheduler and adds the predefined jobs.
    """
    help = "Runs APScheduler."

    def handle(self, *args, **options) -> None:
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            clear_old_notes,
            trigger=CronTrigger(hour="00", minute="00"),    # Midnight every day
            id="clear_old_notes",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
