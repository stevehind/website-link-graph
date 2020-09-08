import networkx as nx
from matplotlib import pyplot as plt

import websitegraph
import scrapedwebsite

class NetworkGraph:
    def __init__(self, url, depth):
        self.url = url
        self.depth = depth

    def return_self_graph(self):
        return websitegraph.WebsiteGraph(self.url).create_graph()

    def create_network_graph(self):
        links = scrapedwebsite.ScrapedWebsite(self.url).formatted_strings()
        graph = self.return_self_graph()

        for link in links:
            link_url = link['url']
            link_graph = websitegraph.WebsiteGraph(link_url).create_graph()

            # Add nodes and edges to original graph
            graph.add_nodes_from(link_graph)
            graph.add_edges_from(link_graph.edges)

        return graph

        ## TODO: nodes that already exist should be merged, rather than showing up as though they're unique
        ## does NetworkX already manage for this? (Check docs)

    def draw_network_graph(self, id):
        graph = self.create_network_graph()
        path_string = './static/images/'
        png_suffix = '.png'

        try:
            nx.draw(graph, with_labels = True, font_size = 6)
            save_path = path_string + id + png_suffix
            plt.savefig(save_path)

            return save_path
        
        except:
            return 'Image not generated.'