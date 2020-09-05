import requests
from bs4 import BeautifulSoup 
from typing import List
import re
import networkx as nx
from matplotlib import pyplot as plt

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

class WebsiteGraph:
    def __init__(self, url, depth):
        self.url = url,
        self.links = ScrapedWebsite(url).formatted_strings()
        self.depth = depth
        self.G = nx.Graph()
    
    def add_url_as_node(self):
        self.G.add_node(self.url[0])
        return self.G
    
    def add_links_as_nodes(self):
        for link in self.links:
            self.G.add_node(link['url'])
        
        return self.G

    def create_graph(self):
        base_node = self.url[0]

        links = self.links
        urls = []

        for link in links:
            url = link['url']
            urls.append(url)
        
        graph = {base_node: urls}

        for key, value in graph.items():
            for value_item in value:
                self.G.add_edge(key, value_item)
        
        return self.G

    def create_network_graph(self):
        # make a graph from the first node
        # make a graph from each first degree connection
        ## set the link as the node
        ## find its links
        ## add each as an edge

    def display_graph(self):
        try:
            graph = self.create_graph()
        
            nx.draw(graph, with_labels = True)
            plt.savefig('./static/images/graph.png')

            return 'Image generated.'
        
        except:
            return 'Image not generated.'


        

        




