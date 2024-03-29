# Stdlib imports
import logging

# Third-party app imports
from flask import Flask, request, jsonify
from flask.ext.cors import CORS
from flask_restful import Resource, Api, reqparse
from raven.contrib.flask import Sentry

# Imports from app
from middleware.config import (
    SENTRY_USER,
    SENTRY_PASSWORD,
    SENTRY_APP_ID,
)
from processing.process_article import process_article
from taskrunner import app as celery_app

# Setting up Flask and API
app = Flask(__name__)
api = Api(app)
CORS(app)

# Setting up Sentry
sentry = Sentry(
    app, dsn='https://' + SENTRY_USER + ':' + SENTRY_PASSWORD + '@app.getsentry.com/' + SENTRY_APP_ID)
logger = logging.getLogger("sentry.errors")
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Setting up parser
parser = reqparse.RequestParser()
parser.add_argument('url')
parser.add_argument('added_by')
parser.add_argument('rss_id')


# Route to POST data for news processing
class Processing(Resource):

    def post(self):
        args = parser.parse_args()
        if 'added_by' in args and args['added_by'] is not None:
            return process_article(args)
        res = celery_app.send_task(
            'processing.process_article.process_article', ([args]))
        return jsonify({'id': res.task_id})

api.add_resource(Processing, '/processing')

if __name__ == '__main__':
    app.run(port=int('8000'), debug=False)
