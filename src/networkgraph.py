import networkx as nx
from matplotlib import pyplot as plt

import websitegraph
import scrapedwebsite

class NetworkGraph:
    def __init__(self, url, depth):
        self.url = url
        self.depth = depth
        self.links = scrapedwebsite.ScrapedWebsite(url).formatted_strings()
        self.graph = websitegraph.WebsiteGraph(url).create_graph()

    def return_self_graph(self):
        return self.graph

    def create_network_graph(self):
        for link in self.links:
            link_url = link['url']
            link_graph = websitegraph.WebsiteGraph(link_url).create_graph()
            
            # Add nodes and edges to original graph
            self.graph.add_nodes_from(link_graph)
            self.graph.add_edges_from(link_graph.edges)

        return self.graph

        ## TODO: nodes that already exist should be merged, rather than showing up as though they're unique
        ## does NetworkX already manage for this? (Check docs)

    def draw_network_graph(self):
        try:
            graph = self.create_network_graph()
        
            nx.draw(graph, with_labels = True, fontsize = 6)
            plt.savefig('./static/images/network_graph.png')

            return 'Image generated.'
        
        except:
            return 'Image not generated.'