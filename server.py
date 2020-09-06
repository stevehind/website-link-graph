from flask import Flask, request, jsonify, Response, render_template
import json
import io
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import string
import random

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'./src'))
from scrapedwebsite import ScrapedWebsite
from websitegraph import WebsiteGraph
from networkgraph import NetworkGraph
from validator_collection import validators, checkers

matplotlib.use('agg')

app = Flask(__name__)

@app.route('/api/v1/healthz', methods = ['GET'])
def hello_world():
    return "API is live!", 200

@app.route('/api/v1/submit_url', methods = ['POST'])
def handle_url():
    request_data = json.loads(request.data)

    url = request_data['url']
    
    if (checkers.is_url(url) != True):
        return Response('Invalid url, please try again.'), 400

    id_length = 8
    request_id = ''.join(random.choice(string.hexdigits + string.digits) for _ in range(id_length))
    request_path = '../../' + NetworkGraph(url, 1).draw_network_graph(request_id)
    print(request_path)

    return render_template('index.html', url = url, request_path = request_path), 200

if (__name__ == '__main__'):
    app.run(host='0.0.0.0', debug = True)