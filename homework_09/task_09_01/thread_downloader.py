import requests
import re

from requests.compat import urljoin
from collections import namedtuple
from threading import Thread
from time import time


COUNTRY_REGEX = r"<div class='item_country.*?'>\s.*?src='(.*?)'>\s.*?<p.*?>.*?</p>\s.*?<p>(.*?)</p>"
Country = namedtuple('Country', [
        'flag_url',
        'name',
    ])


class DownloadThread(Thread):

    def __init__(self, url, name):
        Thread.__init__(self)
        self.name = name
        self.url = url

    def fetch_response_content(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            return response
        else:
            raise ValueError("URL IS INCORRECT")

    def run(self):
        handle = self.fetch_response_content()

        try:
            with open(f'flags/{self.name}.png', 'wb') as out:
                out.write(handle.content)

        except IOError as e:
            print(e)


def load_images_with_threads(main_url):
    response = requests.get(main_url)
    threads = []

    time_start = time()

    for tup in re.findall(COUNTRY_REGEX, response.text):
        country = Country(*tup)
        threads.append(DownloadThread(urljoin(main_url, country.flag_url), country.name))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    time_end = time()

    print(time_end - time_start)


def load_image_linear(main_url):
    response = requests.get(main_url)

    time_start = time()

    for tup in re.findall(COUNTRY_REGEX, response.text):
        country = Country(*tup)
        response_flag = requests.get(urljoin(main_url, country.flag_url))
        with open(f'flags/{country.name}.png', 'wb') as out:
            out.write(response_flag.content)

    time_end = time()

    print(time_end - time_start)


if __name__ == '__main__':
    main_url = 'https://www.countryflags.io'
    load_images_with_threads(main_url)
    load_image_linear(main_url)
