import requests
from typing import List
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from validator_collection import validators, checkers
import time
import sys
import os
import platform

class ScrapedWebsite:
    def __init__(self, url: str):
        self.raw_url = url
        if (checkers.is_url(self.raw_url)):
            if (self.raw_url[-1] != '/'):
                self.url = self.raw_url + '/'
            else:
                self.url = self.raw_url
            
        else:
            raise Exception('Invalid URL')

        ## for selenium headless browser
        # bigger problem: need to have chrome on the deployed os: https://medium.com/@mikelcbrowne/running-chromedriver-with-python-selenium-on-heroku-acc1566d161c
        self.GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
        self.CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--no-sandbox')

        self.chrome_options.binary_location = self.CHROMEDRIVER_PATH

    def return_url(self) -> str:
        return self.url
    
    def return_title(self):
        self.webdriver = webdriver.Chrome(
            executable_path = self.CHROMEDRIVER_PATH, options = self.chrome_options
        )

        wait = WebDriverWait(self.webdriver, 10)

        self.webdriver.get(self.url)

        xpaths = [
            "//title", "//h1", "//h2", "//h3"
        ]

        pot_titles = []

        # try to find titles in the title tag, and in the first header tags
        for xpath in xpaths:
            try:
                title = self.webdriver.find_element_by_xpath(xpath).text
            except:
                title = ''
            pot_titles.append(title)

        # if '' is a title, and all the titles are the same, plug in placeholder test
        if ((pot_titles[0] == '') & (len(set(pot_titles)) == 1)):
            title = 'Could not find a title in <title>, <h1>, <h2> or <h3>'
        # else, iterate through the titles and return the first instance that isn't ''
        else:
            for pot_title in pot_titles:
                if (pot_title != ''):
                    self.webdriver.close()
                    return pot_title
                else:
                    pass
        
    def scrape_raw_links(self) ->  List[str]:
        self.webdriver = webdriver.Chrome(
            executable_path = self.CHROMEDRIVER_PATH, options = self.chrome_options
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
            
            if (checkers.is_url(link)):
                is_external = True
                if (link[-1] == '/'):
                    url = link
                else:
                    url = link + '/'
                title = ScrapedWebsite(link).return_title()
            else:
                is_external = False
                url = link
                title = 'Not an external link'
            
            link_dict = {
                'url': url,
                'title': title,
                'external': is_external
            }

            if ((link_dict['external']) & (link_dict['url'] != self.url)):
                formatted_strings.append(link_dict)

        return formatted_strings