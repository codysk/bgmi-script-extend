# BGmi-script-extend

A BGmi-script extend module

## Usage
Clone from github and place into BGMI_PATH/scripts.
```
cd <BGMI_PATH>/scripts
git clone --recursive https://github.com/codysk/bgmi-script-extend.git ./script_extend
```
Script example see [BGmi-Scripts](https://github.com/codysk/bgmi-scripts.git)

## Extends
You can easily add your own search datasource by extending SearchSource base class and implement one method.
```
# ./search_source/YourSourceName.py
# coding=utf-8
from __future__ import print_function, unicode_literals
import importlib
Base = importlib.import_module('.base', __package__)
class YourSourceName(Base.BaseSearchSource):
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
```
And there is a sample at [./search_source/Nyaa.py](https://github.com/codysk/bgmi-script-extend/blob/master/search_source/Nyaa.py)
