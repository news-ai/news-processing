# Third-party app imports
from newspaper import Article

# Imports from app
from processing.utils.urls import url_validate


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
