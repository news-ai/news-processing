# Stdlib imports
from __future__ import print_function
import json
import os

# Third-party app imports
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from newspaper import Article

# Imports from app
from middleware import config
from processing.utils.urls import url_validate

# Removing requests warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Importing URL
base_url = config.BASE_URL
context_base_url = config.CONTEXT_BASE_URL


def get_login_token(from_discovery):
    headers = {
        "content-type": "application/json",
        "accept": "application/json"
    }
    payload = {
        "username": os.environ.get("NEWSAI_CONTEXT_API_USERNAME"),
        "password": os.environ.get("NEWSAI_CONTEXT_API_PASSWORD"),
    }

    context_url = base_url
    if from_discovery:
        context_url = context_base_url

    r = requests.post(context_url + "/jwt-token/",
                      headers=headers, data=json.dumps(payload), verify=False)
    data = json.loads(r.text)
    token = data.get('token')
    return token


# checking if author exists takes 3 API calls
# we don't want to run into max requests limit issues when we batch process
def read_article_without_author(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    url, publisher = url_validate(url)

    data = {}
    data['url'] = url
    data['name'] = article.title  # Get Title
    if article.publish_date:
        data['created_at'] = str(article.publish_date)
    data['header_image'] = article.top_image
    data['basic_summary'] = article.summary
    data['opening_paragraph'] = article.opening_paragraph
    return data


def read_article(url, token):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    url, publisher = url_validate(url)

    data = {}
    data['url'] = url
    data['name'] = article.title  # Get Title
    if article.publish_date:
        data['created_at'] = str(article.publish_date)
    data['header_image'] = article.top_image
    data['basic_summary'] = article.summary
    data['authors'] = post_author(publisher, article.authors, token)
    return data


def post_article(url, token):
    if token is None:
        print('Missing token')
        return
    headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "authorization": "Bearer " + token
    }

    payload = read_article(url, token)

    r = requests.post(base_url + '/articles/',
                      headers=headers, data=json.dumps(payload), verify=False)
    return r


# checking if author exists takes 3 API calls
# we don't want to run into max requests limit issues when we batch process
# can also post multiples articles in a list
def post_article_without_author(article, token, from_discovery):
    if token is None:
        print('Missing token')
        return

    headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "authorization": "Bearer " + token
    }

    context_url = base_url
    if from_discovery:
        context_url = context_base_url

    payload = article

    r = requests.post(context_url + '/articles/',
                      headers=headers, data=json.dumps(payload), verify=False)
    return r


def is_author_valid(author_name):
    if len(author_name.split(' ')) > 3:
        return False
    return True


def post_author(publisher, authors, token):
    if token is None:
        print('Missing token')
        return

    if len(authors) is 0:
        return []

    headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "authorization": "Bearer " + token
    }

    author_list = []

    for author in authors:
        r = requests.get(base_url + '/authors/?name=' + author + '&writes_for__url=' + publisher,
                         headers=headers, verify=False)
        data = json.loads(r.text)
        if 'results' in data and len(data['results']) > 0:
            author_list.append(data['results'][0])
        else:
            r = requests.get(base_url + '/publishers/?url=' + publisher,
                             headers=headers, verify=False)
            data = json.loads(r.text)
            if 'results' in data and len(data['results']) is 1:
                payload = {
                    'name': author,
                    'publisher': data['results'][0],
                }
                if is_author_valid(author):
                    r = requests.post(base_url + '/authors/',
                                      headers=headers, data=json.dumps(payload), verify=False)
                    data = json.loads(r.text)
                    print(data)
                    author_list.append(data)

    return author_list


def post_publisher(url, name, short_name, is_approved, token, from_discovery):
    if token is None:
        print('Missing token')
        return

    headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "authorization": "Bearer " + token
    }

    context_url = base_url
    if from_discovery:
        context_url = context_base_url

    payload = {
        "url": url,
        'name': name,
        'short_name': short_name,
        'is_approved': is_approved
    }

    r = requests.post(context_url + '/publishers/',
                      headers=headers, data=json.dumps(payload), verify=False)
    return r


def get_publisher(token):
    if token is None:
        print('Missing token')
        return

    headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "authorization": "Bearer " + token
    }

    r = requests.get(base_url + '/publisherfeeds/?limit=1000', headers=headers,
                     verify=False)
    return r
