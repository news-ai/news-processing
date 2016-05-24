# Stdlib imports
from datetime import timedelta

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'UTC'
CELERY_DEFAULT_RATE_LIMIT = '30/m' # 60 tasks per minute
CELERYBEAT_SCHEDULE = {}
