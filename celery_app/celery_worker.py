import smtplib

from celery import Celery
from celery.schedules import crontab
from uuid import UUID
from config import redis_settings, email_settings
from celery_app.email_handler import MessageHandler

celery_app = Celery('tasks', broker=redis_settings.redis_url, backend=redis_settings.redis_url)


@celery_app.task
def send_email_report(report_type: str, username: str = None, user_id: UUID = None, user_email: str = None,
                      groups: list[UUID] = None):
    message_handler = MessageHandler(report_type, groups)
    email = message_handler.get_email_template(username, user_id, user_email=user_email)
    with smtplib.SMTP_SSL(email_settings.email_host, email_settings.email_port) as server:
        server.login(email_settings.email_address, email_settings.email_pass)
        server.send_message(email)


celery_app.conf.beat_schedule = {
    "truant_report": {
        "task": "celery_app.celery_worker.send_email_report",
        "schedule": crontab(hour="9", day_of_month="2"),
        "args": ("truant",)
    }
}
