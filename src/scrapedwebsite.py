import requests
from typing import List
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import sys

class ScrapedWebsite:
    def __init__(self, url: str):
        self.url = url

        ## for selenium headless browser
        self.chrome_driver_path = '/Users/stevenhind/Google Drive/Programming/website-link-graph/chromedriver'

        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')

    def return_url(self) -> str:
        return self.url
    
    def return_title(self):
        self.webdriver = webdriver.Chrome(
            executable_path = self.chrome_driver_path, options = self.chrome_options
        )
        self.webdriver.get(self.url)
        title = self.webdriver.find_element_by_xpath("//title").text
        self.webdriver.close()

        print('The title is:' + title)
        return title
        
    def scrape_raw_links(self) ->  List[str]:
        self.webdriver = webdriver.Chrome(
            executable_path = self.chrome_driver_path, options = self.chrome_options
        )
        self.webdriver.get(self.url)
        raw_links = self.webdriver.find_elements_by_tag_name('a')

        ## TODO: convert to strings
        link_strings = []
        for link in raw_links:
            url = link.get_attribute('href')
            link_strings.append(str(url)) 
        
        self.webdriver.close()

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