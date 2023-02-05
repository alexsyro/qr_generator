from datetime import timedelta
from celery.schedules import crontab
from django.conf import settings

CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

if settings.TESTING:
    CELERY_TASK_ALWAYS_EAGER = True
BROKER_BACKEND = "redis"
BROKER_URL = settings.REDIS_URL
CELERY_RESULT_BACKEND = settings.REDIS_URL


CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_TIMEZONE = 'Europe/Warsaw'

CELERY_IMPORTS = (

)

CELERYBEAT_SCHEDULE = {

}
