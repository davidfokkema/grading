import getpass
import requests
import bs4
import re
from urlparse import urljoin

import logging
logging.basicConfig(level=logging.DEBUG)


class BlackBoard(object):

    """Connect to BlackBoard.

    Connect to BlackBoard and get course listings, lists of students, download
    assignments, etc.

    """

    cookies = None

    def __init__(self, url, user_id):
        """Initialize class.

        :param url: the url of the BlackBoard installation
        :param user_id: the user's id. You will be prompted for you password.

        """
        self.url = url
        self.user_id = user_id
        self.requests = Requests()

    def get_courses(self):
        """Get a list of courses."""

        courses = []

        r, soup = self.open_page(self.url)
        link = soup.find(title=re.compile('Open My Courses'))
        r, soup = self.open_page(urljoin(self.url, link['href']))
        for item in soup.find(class_='courseListing').find_all('li'):
            if not item.find(string='(not currently available)'):
                courses.append(list(item.stripped_strings)[0])
        return courses

    def open_page(self, url):
        """Open the requested page, logging in if necessary.

        Opens the requested url and checks if you have to login. If so, you
        will be prompted for your password and after login the original
        request is performed.

        :param url: the url of the page to open.
        :returns request, soup: returns the request object and the results
            from BeautifulSoup.

        """
        r, soup = self.requests.get(url)
        logging.debug("GET %s" % self.url)

        while self.is_login_page(soup):
            logging.debug("POST %s (%s)" % (self.url, self.user_id))
            password = getpass.getpass()
            r, soup = self.requests.post(self.url,
                                         data={'user_id': self.user_id,
                                               'password': password})

        return r, soup

    def is_login_page(self, soup):
        """Check if a page is a login landing page.

        If you open a page, you might be redirected to the login page. This
        method checks if that is the case.

        :param soup: the BeautifulSoup output of the requests
        :returns boolean: True if this is a login page

        """
        if soup.find('input', value=re.compile('login')):
            return True
        else:
            return False


class Requests(object):

    """Container for requests returning BeautifulSoup output."""

    def __init__(self):
        self.session = requests.Session()

    def get(self, url):
        """Get the contents of an url.

        :param url: the url of the page to access
        :returns request, soup: returns the request object and the results
            from BeautifulSoup.

        """
        r = self.session.get(url)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        return r, soup

    def post(self, url, data):
        """Post data to an url.

        :param url: url to post data to
        :param data: the data
        :returns request, soup: returns the request object and the results
            from BeautifulSoup.

        """
        r = self.session.post(url, data)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        return r, soup


if __name__ == '__main__':
    bb = BlackBoard('https://bb.vu.nl', 'dfa210')
    bb.get_courses()
