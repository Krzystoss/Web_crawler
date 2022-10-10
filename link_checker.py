import pandas as pd
from scrapper import Scrapper


class LinkChecker:

    def __init__(self, file_format, output):
        self.file_format = file_format
        self.output = output

    def check_link(self, url):
        print(f"Scrapping: {url}")
        dictionary = self.scrape_url(url, {})
        not_visited_link = self.find_not_visited_link(dictionary)
        number_of_links_counter = 0
        while not_visited_link is not None:
            print(f"Scrapping: {not_visited_link}")
            dictionary = self.scrape_url(not_visited_link, dictionary)
            not_visited_link = self.find_not_visited_link(dictionary)
            number_of_links_counter += 1
            if number_of_links_counter % 100 == 0:
                self.save_file(pd.DataFrame(list(dictionary.values())))
                print("Saved current progress")
        self.save_file(pd.DataFrame(list(dictionary.values())))
        return dictionary

    def scrape_url(self, url, urls_dictionary):
        return Scrapper(url, self.file_format, self.output, urls_dictionary).start_crawl()

    def find_not_visited_link(self, urls_dictionary):
        for link in urls_dictionary.keys():
            if urls_dictionary[link]['internal links count'] == -1:
                return link

    def save_file(self, file):
        if self.file_format == 'CSV':
            file.to_csv(self.output, index=False)
        if self.file_format == 'JSON':
            file.to_json(self.output, index=False, orient='split')
