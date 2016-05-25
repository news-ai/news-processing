# Stdlib imports
import json
import logging
from urlparse import urlparse
from taskrunner import app

# Imports from app
from processing.internal.context import (
    get_login_token,
    post_publisher,
    read_article_without_author,
    post_article_without_author,
)
from middleware.config import BASE_URL


@app.task
def process_article(args):
    stops = ['www', 'com', 'org', 'io']
    url = urlparse(args['url']).netloc
    name = [w for w in url.split('.')
            if w not in stops][0]
    short_name = name[0:5]
    is_approved = False
    token = get_login_token(True)

    from_discovery = False
    if 'added_by' in args and args['added_by'] is not None:
        from_discovery = True

    pr = post_publisher(
        'http://' + url,
        name,
        short_name,
        is_approved,
        token,
        from_discovery)

    article = read_article_without_author(args['url'])
    article['authors'] = []
    if from_discovery:
        article['added_by'] = BASE_URL + '/users/' + \
            str(args['added_by']) + '/'
    articles = []
    articles.append(article)
    ar = post_article_without_author(article, token, from_discovery)
    return ar.json()
