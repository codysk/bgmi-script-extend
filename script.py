# coding=utf-8
from __future__ import print_function, unicode_literals

import datetime, re, os, imp
import importlib
from bgmi.script import ScriptBase
from bgmi.lib.fetch import DATA_SOURCE_MAP
file, pathname, desc = imp.find_module('search_source', [os.path.split(os.path.realpath(__file__))[0]])
imp.load_module('search_source', file, pathname, desc)
import search_source.base as search_base

class SearchScriptBase(ScriptBase):
    class Model(ScriptBase.Model):
        """
        bangumi_name = '我喜歡的妹妹不是妹妹'
        cover = 'http://lain.bgm.tv/pic/cover/l/ef/68/228255_k7ex1.jpg'
        update_time = 'Wed'
        due_date = datetime.datetime(2019, 1, 1)
        source = 'dmhy'
        keyword = 'imouto ja nai'

        include_regex_filters = [
            r'(BIG5|繁体|繁體)',
        ];

        exclude_regex_filters = [
            r'(HEVC|MKV|H265)',
        ];
        """
        pre_fetch_hooks = [
            # method_name,
        ]
        post_fetch_hooks = [
            # method_name,
        ]
        post_get_download_url_hooks = [
            # method_name,
        ]
    
    def regex_filter(self, title='', include_regex_filters=[], exclude_regex_filters=[]):
        for regex in include_regex_filters:
            if not re.search(regex, title):
                if os.getenv('TEST_RUN'):
                    print('filter by include_regex_filters')
                return False;
            pass

        for regex in exclude_regex_filters:
            if re.search(regex, title):
                if os.getenv('TEST_RUN'):
                    print('filter by exclude_regex_filters')
                return False;
            pass
        return True


    def get_download_url(self):
        """Get the download url, and return a dict of episode and the url.
        Download url also can be magnet link.
        For example:
        ```
            {
                1: 'http://example.com/Bangumi/1/1.mp4'
                2: 'http://example.com/Bangumi/1/2.mp4'
                3: 'http://example.com/Bangumi/1/3.mp4'
            }
        ```
        The keys `1`, `2`, `3` is the episode, the value is the url of bangumi.
        :return: dict
        """
        if self.source is not None:
            source = self.get_source(self.source)
            ret = {}

            # call pre_fetch_hooks
            for method_name in self.Model.pre_fetch_hooks:
                if os.getenv('TEST_RUN'):
                    print("calling %s" % method_name)
                method = getattr(self.Model, method_name)
                method(self)
                pass

            # fetch
            data = source.search_by_keyword(self.Model.keyword)

            # call post_fetch_hooks
            for method_name in self.Model.post_fetch_hooks:
                if os.getenv('TEST_RUN'):
                    print("calling %s" % method_name)
                method = getattr(self.Model, method_name)
                method(self, data)
                pass

            if os.getenv('TEST_RUN'):
                print(data)
            for i in data:
                if os.getenv('TEST_RUN'):
                    print(i['title'])

                if not self.regex_filter(
                    title=i['title'],
                    include_regex_filters=self.Model.include_regex_filters, 
                    exclude_regex_filters=self.Model.exclude_regex_filters
                ):
                    continue;

                if int(i['episode']) > 2000:
                    if os.getenv('TEST_RUN'):
                        print('invalid episode: %d' % (i['episode']))
                    continue;
                if int(i['episode']) in ret.keys():
                    if os.getenv('TEST_RUN'):
                        print('pass all cond. but episode %d existed' % (i['episode']))
                    continue;
                if os.getenv('TEST_RUN'):
                    print('pass all cond.')
                ret[int(i['episode'])] = i['download']

            # call post_get_download_url_hooks
            for method_name in self.Model.post_get_download_url_hooks:
                if os.getenv('TEST_RUN'):
                    print("calling %s" % method_name)
                method = getattr(self.Model, method_name)
                method(self, ret)
                pass

            return ret
        else:
            return {}

    def get_source(self, source):
        try:
            source_instance = DATA_SOURCE_MAP.get(source, None)()
            return source_instance
        except Exception as e:
            source_instance = None


        try:
            source_instance = importlib.import_module('search_source.%s' % (source))
            source_instance = getattr(source_instance, source)()
        except Exception as e:
            source_instance = None

        if source_instance is None:
                raise Exception('Script data source is invalid, usable subscript sources: {}; search sources: {}'
                               .format((', '.join(DATA_SOURCE_MAP.keys())), (',').join(search_base.sources())))
        
        return source_instance


if __name__ == '__main__':
    os.environ["TEST_RUN"] = '1'
    s = SearchScriptBase()
    print(s.get_download_url())