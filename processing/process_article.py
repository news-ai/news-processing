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
from middleware.config import CONTEXT_BASE_URL


@app.task
def process_article(args):
    stops = ['www', 'com', 'org', 'io']
    url = urlparse(args['url']).netloc
    name = [w for w in url.split('.')
            if w not in stops][0]
    short_name = name[0:5]
    is_approved = False
    token = get_login_token(True)
    pr = post_publisher(
        'http://' + url,
        name,
        short_name,
        is_approved,
        token,
        True)
    article = read_article_without_author(args['url'])
    article['authors'] = []
    if 'added_by' in args and len(args['added_by']) is not 0:
        article['added_by'] = CONTEXT_BASE_URL + '/users/' + \
            str(args['added_by']) + '/'
    articles = []
    articles.append(article)
    ar = post_article_without_author(articles, token, True)
    return ar.json()
