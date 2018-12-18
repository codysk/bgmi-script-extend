# coding=utf-8
from __future__ import print_function, unicode_literals

import re, os, json
import importlib
import search_source.base as Base

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

class Zimuzu_id(Base.BaseSearchSource):

    base_url = "http://pc.allappapi.com/index.php"

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

        result = []
        
        params = {
            "g": 'api/pv2',
            "m": 'index',
            "a": "resource",
            "accesskey": "519f9cab85c8059d17544947k361a827",
            "id": keyword
        }

        if os.environ.get('DEBUG', False):  # pragma: no cover
            print(self.base_url, params)

        content = fetch_url(self.base_url, params=params)
        
        data_struct = json.loads(content)

        name = data_struct['data']['detail']['cnname']

        episodes = self.get_episodes(data_struct['data']['list'])

        if os.environ.get('DEBUG', False):
            print(episodes)

        for episode in episodes:

            title, download = self.get_title_and_download_link(episode['files']['MP4'])

            res = {
                'name': name,
                'download': download,
                'title': title,
                'episode': episode['episode']
            }
            result.append(res)
            pass

        if os.environ.get('DEBUG', False):  # pragma: no cover
            print(result)

        return result

    def get_episodes(self, session_list):
        for item in session_list:
            if item['season'] == "101":
                return item['episodes']
            pass
        return None

    def get_title_and_download_link(self, mp4_file_list):
        for item in mp4_file_list:
            if item['way'] == "2":
                return (item['name'], item['address'])
            pass
        return None

    pass
    

