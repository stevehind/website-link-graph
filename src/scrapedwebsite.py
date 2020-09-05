import requests
from bs4 import BeautifulSoup 
from typing import List
import re
import networkx as nx
from matplotlib import pyplot as plt
import websitegraph

class ScrapedWebsite:
    def __init__(self, url: str):
        self.url = url
        ## TODO: Fix this
        try:
            request = requests.get(url)
        except:
            request = requests.get('https://www.example.com')
        self.soup = BeautifulSoup(request.content, 'html5lib')

    def return_url(self) -> str:
        return self.url

    def return_page(self):
        return self.soup

    def return_title(self):
        try:
            # TODO: regex this to remove the title tags
            raw_title = self.soup.find('title') 
        except:
            raw_title = ''

        return str(raw_title)

    def scrape_raw_links(self) ->  List[str]:
        raw_links = self.soup('a')
        link_strings = []
        for link in raw_links:
            link_strings.append(str(link)) 
        return link_strings
    
    def formatted_strings(self) -> List[dict]:
        link_strings = self.scrape_raw_links()
        formatted_strings = []

        for link in link_strings:
            # Sample string to parse
            # '<a href="https://www.iana.org/domains/example">More information...</a>'
            try:
                url = re.search(r'a href="(.*?)">', link).group(1)
            ## TODO: change this
            except:
                url = ''
            
            # Fill in the title later when scraping the link itself?
            title = ScrapedWebsite(url).return_title()
            
            if (url[0:4] == 'http'):
                is_external = True
                url = url
            else:
                is_external = False
                url = ''
            
            link_dict = {
                'url': url,
                'title': title,
                'external': is_external
            }

            if (link_dict['external']):
                formatted_strings.append(link_dict)

        return formatted_strings