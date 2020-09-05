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
        ## TODO: Fix this
        try:
            request = requests.get(url)
        except:
            request = requests.get('https://www.example.com')

        ## for selenium headless browser
        self.chrome_driver_path = '/Users/stevehind/Google Drive/Programming/website-link-graph/chromedriver'

        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.webdriver = webdriver.Chrome(
            executable_path = self.chrome_driver_path, options = self.chrome_options
        )

    def return_url(self) -> str:
        return self.url

    def return_page(self):
        # return self.soup
        ## scrape the website
        with webdriver as driver:
            # Set timeout time 
            wait = WebDriverWait(driver, 10)
            # retrive url in headless browser
            return driver.get(self.url)
            
            # close
            driver.close()

    def return_title(self):
        try:
            # TODO: regex this to remove the title tags
            raw_title = self.return_page().find_element_by_id('title')
        except:
            raw_title = ''

        return str(raw_title)

    def scrape_raw_links(self) ->  List[str]:
        raw_links = self.return_title().find_element_by_id('a')
        print(raw_links)

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