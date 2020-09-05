import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../src'))
import scrapedwebsite

target_url = 'https://www.stevehind.me'
website = scrapedwebsite.ScrapedWebsite(target_url)

def test_correctly_retrieves_url():
    assert website.return_url() == target_url 

def test_scrape_raw_links():
    links = website.scrape_raw_links()
    assert links[0:2] == [
        '<a class="navbar-brand" href="/">stevehind.me</a>',
        '<a href="https://stevehind-dog-merch.builtwithdark.com">dog-merch</a>'
    ]

def test_extracts_formatted_links():
    links = website.formatted_strings()

    assert links[0] == {
        'url':  'https://stevehind-dog-merch.builtwithdark.com',
        'title': '<title>Buy Sydney and Sesil Merch!</title>',
        'external': True
    }