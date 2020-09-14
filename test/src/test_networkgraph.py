import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../src'))
import networkgraph

univ_url = 'https://www.stevehind.me'

def test_creates_self_graph():
    url = 'https://stevehind.github.io/sms-steve/'
    nwgraph = networkgraph.NetworkGraph(url, 1)
    self_graph = nwgraph.return_self_graph()
    assert(list(self_graph.nodes)) == ['https://stevehind.github.io/sms-steve/', 'http://www.stevehind.me/']

def test_creates_network_graph():
    url = 'https://stevehind.github.io/sms-steve/'
    nwgraph = networkgraph.NetworkGraph(url, 1)
    graph = nwgraph.create_network_graph()
    target_nodes = ['https://stevehind.github.io/sms-steve/', 'http://www.stevehind.me/', 'https://stevehind-dog-merch.builtwithdark.com/', 'https://stevehind-fifa-stats.builtwithdark.com/', 'https://stevehind-betting-odds.builtwithdark.com/register', 'http://www.twitter.com/stevehind', 'http://www.linkedin.com/in/shind', 'http://www.github.com/stevehind', 'http://www.medium.com/@stevehind']
    target_edges = [('https://stevehind.github.io/sms-steve/', 'http://www.stevehind.me/'), ('http://www.stevehind.me/', 'https://stevehind-dog-merch.builtwithdark.com/'), ('http://www.stevehind.me/', 'https://stevehind-fifa-stats.builtwithdark.com/'), ('http://www.stevehind.me/', 'https://stevehind-betting-odds.builtwithdark.com/register'), ('http://www.stevehind.me/', 'http://www.twitter.com/stevehind'), ('http://www.stevehind.me/', 'http://www.linkedin.com/in/shind'), ('http://www.stevehind.me/', 'http://www.github.com/stevehind'), ('http://www.stevehind.me/', 'http://www.medium.com/@stevehind')]

    # Don't need nodes to be in same order as provided in test, just for it to contain all the nodes
    assert len(list(graph.nodes)) == len(target_nodes)
    assert list(graph.nodes) == target_nodes

    assert(list(graph.edges)) == target_edges

def test_draws_network_graph():
    url = 'https://stevehind.github.io/sms-steve/'
    nwgraph = networkgraph.NetworkGraph(url, 1)
    test_id = 'test_simple_graph'

    graph_msg = nwgraph.draw_network_graph(test_id)

    assert(graph_msg) == 'Image saved to s3 bucket as ' + test_id + '.png'

def test_draws_more_complex_network_graph():
    test_id = 'test_complex_graph'
    nwgraph = networkgraph.NetworkGraph(univ_url, 1)
    graph_msg = nwgraph.draw_network_graph(test_id)

    assert(graph_msg) == './static/images/' + test_id + '.png'