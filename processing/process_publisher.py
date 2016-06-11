# Stdlib imports
import urllib2

# Third-party app imports
from bs4 import BeautifulSoup


def get_publisher_title(url):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    return soup.title and soup.title.string
