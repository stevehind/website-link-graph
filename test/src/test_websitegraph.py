import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../src'))
from scrapedwebsite import ScrapedWebsite
from websitegraph import WebsiteGraph

target_url = 'https://www.stevehind.me'
website = ScrapedWebsite(target_url)
graph = WebsiteGraph(target_url, 1)

def test_returns_graph():
    graph_with_node = graph.add_url_as_node()
    assert list(graph_with_node.nodes)[0] == target_url

# Should really decouple this from above test, e.g. right now the test implicitly requires the test above to have run.
def test_adds_links_as_nodes():
    graph_with_links_as_nodes = graph.add_links_as_nodes()
    assert list(graph_with_links_as_nodes.nodes)[0:3] == [
        'https://www.stevehind.me',
        'https://stevehind-dog-merch.builtwithdark.com',
        'https://stevehind.github.io/sms-steve/'
    ]
    assert len(list(graph_with_links_as_nodes.nodes)) == 9

def test_create_graph_addes_edges():
    graph_with_edges_between_nodes = graph.create_graph()
    assert list(graph_with_edges_between_nodes.edges)[0:3] == [
        ('https://www.stevehind.me','https://stevehind-dog-merch.builtwithdark.com'),
        ('https://www.stevehind.me','https://stevehind.github.io/sms-steve/'),
        ('https://www.stevehind.me','https://stevehind-fifa-stats.builtwithdark.com')
    ]

def test_output_graph():
    graph_image = graph.display_graph()
    assert graph_image == 'Image generated.'
