import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../src'))
import scrapedwebsite
import pytest

target_url =  'https://stevehind.github.io/sms-steve/'
website = scrapedwebsite.ScrapedWebsite(target_url)

def test_raises_exception_for_invalid_url():
    with pytest.raises(Exception):
        scrapedwebsite.ScrapedWebsite('foo bar')

def test_correctly_retrieves_url():
    assert website.return_url() == target_url 

def test_returns_title():
    assert website.return_title() == 'Just like using your phone...'

def test_scrape_raw_links():
    links = website.scrape_raw_links()

    assert links == [
        'http://www.stevehind.me/'
    ]

def test_extracts_formatted_links():
    links = website.formatted_strings()

    assert links[0] == {
        'url':  'http://www.stevehind.me/',
        'title': "Steve's jankey website",
        'external': True
    }

def test_does_not_include_links_to_self():
    test_url = 'http://www.stevehind.me/'
    website = scrapedwebsite.ScrapedWebsite(test_url)

    links = website.formatted_strings()

    assert test_url not in links

def test_appends_slash_to_valid_url():
    test_url = 'https://www.stevehind.me'
    website = scrapedwebsite.ScrapedWebsite(test_url)

    assert website.return_url() == 'https://www.stevehind.me/'