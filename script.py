# coding=utf-8
from __future__ import print_function, unicode_literals

import datetime, re, os, imp
import importlib
from bgmi.script import ScriptBase
from bgmi.lib.fetch import DATA_SOURCE_MAP
file, pathname, desc = imp.find_module('search_source', [os.path.split(os.path.realpath(__file__))[0]])
imp.load_module('search_source', file, pathname, desc)
import search_source

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
            data = source.search_by_keyword(self.Model.keyword)
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
                        print('invalid episode: %d' %(i['episode']))
                    continue;
                if int(i['episode']) not in data:
                    if os.getenv('TEST_RUN'):
                        print('pass all cond.')
                    ret[int(i['episode'])] = i['download']
            return ret
        else:
            return {}

    def get_source(self, source):
        try:
            source_instance = DATA_SOURCE_MAP.get(source, None)()
            return source_instance
        except Exception as e:
            source_instance = None
        
        source_instance = importlib.import_module('search_source.%s' % (source))
        source_instance = getattr(source_instance, source)()

        if source_instance is None:
                raise Exception('Script data source is invalid, usable sources: {}'
                               .format(', '.join(DATA_SOURCE_MAP.keys())))
        
        return source_instance

if __name__ == '__main__':
    os.environ["TEST_RUN"] = '1'
    s = SearchScriptBase()
    print(s.get_download_url())