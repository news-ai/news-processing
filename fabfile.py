from fabric.api import *

env.hosts = []

env.user = "api"


def update_upgrade():
    """
        Update the default OS installation's
        basic default tools.
    """
    run("sudo apt update")
    run("sudo apt -y upgrade")


def update_server():
    update_upgrade()


def get_logs():
    get('/var/apps/log', '%(path)s')


def celery_purge():
    with cd("/var/apps/news-processing"), prefix('source /var/apps/news-processing/env/bin/activate'):
        with cd("/var/apps/news-processing/news-processing"):
            run('echo yes | celery -A taskrunner purge && supervisorctl restart workers:celeryd1 workers:celeryd2')


def deploy():
    with cd("/var/apps/news-processing"), prefix('source /var/apps/news-processing/env/bin/activate'):
        with cd("/var/apps/news-processing/news-processing"):
            run('git pull origin master')
            run('pip install -r requirements.txt')
            run('supervisorctl reread')
            run('supervisorctl update')
            run('supervisorctl restart api workers:celeryd1 workers:celeryd2')
