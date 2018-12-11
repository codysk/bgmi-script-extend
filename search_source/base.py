# coding=utf-8
from __future__ import print_function, unicode_literals

import pkgutil, sys
from bgmi.website.base import BaseWebsite
from bgmi.config import (MAX_PAGE, IS_PYTHON3)

def get_available_search_source_list():
    for importer, modname, ispkg in pkgutil.iter_modules(sys.modules[__package__].__path__):
        if ispkg == False and modname != 'base':
            yield modname
    pass

def sources():
    return [source for source in get_available_search_source_list()]

class BaseSearchSource(BaseWebsite):
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
        raise NotImplementedError
        