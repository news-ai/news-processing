# Stdlib imports
import os

BASE_URL = 'https://internal.newsai.org/api'
CONTEXT_BASE_URL = 'https://context.newsai.org/api'
CONTEXT_API_USERNAME = os.environ.get('NEWSAI_CONTEXT_API_USERNAME')
CONTEXT_API_PASSWORD = os.environ.get('NEWSAI_CONTEXT_API_PASSWORD')

SENTRY_USER = 'a1470015603f469faf398e861a887f0d'
SENTRY_PASSWORD = '37fa444462f142008ba58e488679c9b4'
SENTRY_APP_ID = '76018'

EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_USERNAME = 'celery@dev.newsai.org'
EMAIL_PASSWORD = 'MA6qGNFyZiZoeUAT}N4v'
