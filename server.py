from flask import Flask, request, jsonify, Response, render_template
import json
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'./src'))
from scrapedwebsite import ScrapedWebsite
from websitegraph import WebsiteGraph

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def hello_world():
    return "Hello, world!"

@app.route('/api/v1/submit_url', methods = ['POST'])
def handle_url():
    request_data = json.loads(request.data)

    url = request_data['url']
    print('Request url is: '+ url)

    graph = WebsiteGraph(url, 1)
    graph_image = graph.display_graph

    return render_template('index.html', url = url)

if (__name__ == '__main__'):
    app.run(host='0.0.0.0', debug = True)