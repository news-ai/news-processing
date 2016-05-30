# Stdlib imports
import json
import logging
from urlparse import urlparse
from taskrunner import app

# Imports from app
from processing.internal.context import (
    get_login_token,
    post_publisher,
    post_article_without_author,
)
from processing.articles import (
    read_article_without_author,
)
from middleware.config import BASE_URL


@app.task
def process_article(args):
    stops = ['www', 'com', 'org', 'io']
    url = urlparse(args['url']).netloc
    name = [w for w in url.split('.')
            if w not in stops][0]
    short_name = name[0:5].upper()
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

    # HTTPS requires a verify. Simple fix for now.
    article_url = args['url']
    article_url = article_url.replace('https://', 'http://')

    article = read_article_without_author(article_url)
    article['authors'] = []

    if 'rss_id' in args and args['rss_id'] is not None:
        publisher_feed_url = BASE_URL + \
            '/publisherfeeds/' + str(args['rss_id']) + '/'
        article['publisher_feed'] = publisher_feed_url

    if from_discovery:
        article['added_by'] = BASE_URL + '/users/' + \
            str(args['added_by']) + '/'
    articles = []
    articles.append(article)
    ar = post_article_without_author(article, token, from_discovery)
    return ar.json()
