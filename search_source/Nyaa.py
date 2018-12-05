# coding=utf-8
from __future__ import print_function, unicode_literals

import re, os
import importlib
Base = importlib.import_module('.base', __package__)

import requests
from bgmi.utils import print_error
from bs4 import BeautifulSoup

def fetch_url(url, **kwargs):
        ret = None
        try:
            ret = requests.get(url, **kwargs).text
        except requests.ConnectionError:
            print_error('Create connection to {site}... failed'.format(site=base_url))

        return ret

class Nyaa(Base.BaseSearchSource):

    base_url = "https://nyaa.si/"

    def search_by_keyword(self, keyword, count=None):
        """
        return a list of dict with at least 4 key: download, name, title, episode
        example:
        ```
            [
                {
                    'name':"路人女主的养成方法",
                    'download': 'magnet:?xt=urn:btih:what ever',
                    'title': "[澄空学园] 路人女主的养成方法 第12话 MP4 720p  完",
                    'episode': 12
                },
            ]

        :param keyword: search key word
        :type keyword: str
        :param count: how many page to fetch from website
        :type count: int

        :return: list of episode search result
        :rtype: list[dict]
        """
        if type(count) != int :
            count = 3

        search_url = self.base_url

        result = []
        for i in range(count):
            params = {
                "f": '0',
                "c": '0_0',
                "q": keyword,
                "p": i + 1 # nyaa page base on 1, not 0
            }

            if os.environ.get('DEBUG', False):  # pragma: no cover
                print(search_url, params)

            content = fetch_url(search_url, params=params)
            bs = BeautifulSoup(content, 'lxml')

            tr_list = bs.find_all('tr', {'class': 'default'})

            for tr in tr_list:
                td_list = tr.find_all('td')

                name = keyword
                title = td_list[1].find('a').get_text(strip=True)
                download = td_list[2].find_all('a')[1]['href']
                episode = self.parse_episode(title)
                time = int(td_list[4]['data-timestamp'])

                result.append({
                    'name': name,
                    'title': title,
                    'download': download,
                    'episode': episode,
                    'time': time,
                })

                pass
            pass

        if os.environ.get('DEBUG', False):  # pragma: no cover
            print(result)

        return result
    pass
    

