import re
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import os


class Scrapper:

    def __init__(self, url, file_format, output, urls_dictionary):
        # self.url = url
        self.url = url[:-1] if url[-1] == '/' else url
        self.file_format = file_format
        self.output = output
        self.urls_dictionary = urls_dictionary

    def start_crawl(self):
        try:
            page = get(self.url)
        except Exception:
            self.update_main_link('error', 'error', 'error')
            return self.urls_dictionary
        bs = BeautifulSoup(page.content, 'html.parser')
        if bs.find("title") is not None:
            page_title = bs.find("title").get_text()
        else:
            page_title = ''
        external_links_counter = 0
        internal_links_counter = 0
        external_links_condition = "^http.*"
        for link in self.get_uniqe_links(bs):
            if re.match(external_links_condition, link):
                external_links_counter += 1
            else:
                internal_links_counter += 1
                self.update_reference_counter(self.url + link)
        self.update_main_link(external_links_counter, internal_links_counter, page_title)
        return self.urls_dictionary

    def update_main_link(self, external_links_counter, internal_links_counter, page_title):
        main_url = self.url + "/" if (self.url + "/") in self.urls_dictionary.keys() else self.url
        ref_counter = 0 if main_url not in self.urls_dictionary.keys() else self.urls_dictionary[main_url][
            'reference count']
        self.urls_dictionary[main_url] = self.create_row(main_url, page_title, internal_links_counter,
                                                         external_links_counter, ref_counter)

    def update_reference_counter(self, link):
        if link in self.urls_dictionary.keys():
            self.urls_dictionary[link]['reference count'] += 1
        else:
            self.urls_dictionary[link] = self.create_row(link, '', -1, -1, 1)

    def read_file(self):
        if os.path.isfile(self.output):
            if self.file_format == 'CSV':
                return pd.read_csv(self.output)
            if self.file_format == 'JSON':
                return pd.read_json(self.output)
        else:
            return pd.DataFrame(
                columns=['url', 'title', 'internal links count', 'external links count', 'reference count'],
                index=[0])

    def create_dictionary_from_dataframe(self, data_frame):
        dictionary = {}
        for index, row in data_frame.iterrows():
            dictionary[row['url']] = {'url': row['url'], 'title': row['title'],
                                      'internal links count': row['internal links count'],
                                      'external links count': row['external links count'],
                                      'reference count': row['reference count']}
        return dictionary

    def create_row(self, link, page_title, internal_links_counter, external_links_counter, reference_count):
        d = {'url': link, 'title': page_title,
             'internal links count': internal_links_counter,
             'external links count': external_links_counter,
             'reference count': reference_count}
        return d

    def get_uniqe_links(self, bs):

        unique_links = set()
        for link in bs.find_all('a'):
            link = link.get('href')
            if link is not None and len(link) > 1 and "?" not in link and '/..' not in link:
                link = link[:-1] if link[-1] == '/' and link[-2] != '/' else link
                unique_links.add(link)
        return unique_links
