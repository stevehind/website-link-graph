import requests
from bs4 import BeautifulSoup 
from typing import List
import re
import networkx as nx
from matplotlib import pyplot as plt
import scrapedwebsite

class WebsiteGraph:
    def __init__(self, url):
        self.url = url,
        self.links = scrapedwebsite.ScrapedWebsite(url).formatted_strings()
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

    def display_graph(self):
        try:
            graph = self.create_graph()
        
            nx.draw(graph, with_labels = True)
            plt.savefig('./static/images/graph.png')

            return 'Image generated.'
        
        except:
            return 'Image not generated.'