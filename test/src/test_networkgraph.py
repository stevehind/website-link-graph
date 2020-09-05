import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../src'))
import networkgraph

url = 'https://www.stevehind.me'
nwgraph = networkgraph.NetworkGraph(url, 1)

target_nodes = [
    'https://www.stevehind.me', 'https://stevehind-dog-merch.builtwithdark.com', 'https://stevehind.github.io/sms-steve/', 'https://stevehind-fifa-stats.builtwithdark.com', 'https://stevehind-betting-odds.builtwithdark.com/register', 'http://www.twitter.com/stevehind', 'http://www.linkedin.com/in/shind', 'http://www.github.com/stevehind', 'http://www.medium.com/@stevehind', 'https://avatars3.githubusercontent.com/u/17911380?s=400&amp;u=c56c6ac76fe8d4ca5118f8a49a251589436d01d1&amp;v=4" itemprop="image', 'https://docs.github.com/en/articles/blocking-a-user-from-your-personal-account', 'https://docs.github.com/en/articles/reporting-abuse-or-spam', 'https://docs.github.com/categories/setting-up-and-managing-your-github-profile'
]

def test_creates_network_graph():
    graph = nwgraph.create_network_graph()

    assert(list(graph.nodes)) == target_nodes
    assert(list(graph.edges)) == 'foo'

# def test_draws_network_graph():
#     graph_msg = nwgraph.draw_network_graph()

#     assert(graph_msg) == 'Image generated.'