import networkx as nx
from matplotlib import pyplot as plt
import os
import io

import websitegraph
import scrapedwebsite

import boto3
from botocore.config import Config

config = Config(
    region_name = 'us-west-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

s3 = boto3.resource('s3',
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
)
target_bucket = os.getenv('S3_BUCKET')


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

        try:            
            nx.draw(graph, with_labels = True, font_size = 6)

            img_data = io.BytesIO()
            plt.savefig(img_data, format = 'png')
            img_data.seek(0)
            
            s3.Bucket(target_bucket).put_object(Body = img_data, ContentType = 'image/png', Key = id)

            return 'Image saved to s3 bucket as ' + id + '.png'
        
        except:
            return 'Image not generated.'