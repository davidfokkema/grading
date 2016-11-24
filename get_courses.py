import getpass
import requests
import bs4
import re
from urlparse import urljoin

import logging
logging.basicConfig(level=logging.DEBUG)


class BlackBoard(object):

    cookies = None

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id
        self.requests = Requests()

    def get_courses(self):
        r, soup = self.open_page(self.url)
        link_text = soup.find(string='Courses')
        link = link_text.find_parent('a')['href']
        r, soup = self.open_page(urljoin(self.url, link))
        self.r, self.soup = r, soup

    def open_page(self, url):
        r, soup = self.requests.get(url)
        logging.debug("GET %s" % self.url)

        while self.is_login_page(soup):
            logging.debug("POST %s (%s)" % (self.url, self.user_id))
            password = getpass.getpass()
            r, soup = self.requests.post(self.url,
                data={'user_id': self.user_id, 'password': password})

        return r, soup

    def is_login_page(self, soup):
        if soup.find('input', value=re.compile('login')):
            return True
        else:
            return False


class Requests(object):

    def __init__(self):
        self.session = requests.Session()

    def get(self, url):
        r = self.session.get(url)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        return r, soup

    def post(self, url, data):
        r = self.session.post(url, data)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        return r, soup


if __name__ == '__main__':
    if 'bb' not in globals():
        bb = BlackBoard('https://bb.vu.nl', 'dfa210')
    bb.get_courses()
