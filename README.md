# news-processing

Processing new news articles

Run Celery with: `celery worker -A taskrunner --beat -l info -c 5`

Start Redis: `redis-server`

Check if it's running: `redis-cli ping`

To run a purge on current tasks: `celery -A taskrunner purge`
