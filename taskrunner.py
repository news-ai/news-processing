# Third-party app imports
from celery import Celery

# Imports from app
import celeryconfig


def make_celery():
    celery = Celery(
        'taskrunner',
        broker='redis://localhost:6379/0',
        include=['processing.process_article'],
    )
    celery.config_from_object(celeryconfig)
    return celery


app = make_celery()
