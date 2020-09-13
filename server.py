from flask import Flask, request, jsonify, Response, render_template
import json
import io
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import string
import random
from validator_collection import validators, checkers

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'./src'))

# rq queue
from rq import Queue
from worker import conn

# internal functions
import networkgraph 

matplotlib.use('agg')

# app
app = Flask(__name__)

# establish worker queue
q = Queue(connection=conn)

@app.route('/', methods = ['GET'])
def home():
    return "Nothing to see here, move along.", 200

@app.route('/api/v1/healthz', methods = ['GET'])
def healthz():
    return "API is live!", 200

@app.route('/api/v1/submit_url', methods = ['POST'])
def submit_url():
    request_data = json.loads(request.data)
    url = request_data['url']
    
    if (checkers.is_url(url) != True):
        return Response('Invalid url, please try again.'), 400

    id_length = 8
    request_id = ''.join(random.choice(string.hexdigits + string.digits) for _ in range(id_length))

    nwgraph = networkgraph.NetworkGraph(url, 1)
    if (nwgraph):
        print('There was a nwgraph here!')
        job = q.enqueue(networkgraph.NetworkGraph(url,1).draw_network_graph, request_id,
            job_timeout = '1h',
            job_id = request_id
        )
    else:
        return 'Could not instantiate networkgraph object.', 500

    return 'Processing in background. View result in about 10 minutes at: http://0.0.0.0:5000/api/v1/submit_url/' + request_id, 200

@app.route('/api/v1/submit_url/<string:request_id>', methods = ['GET'])
def display_job(request_id):
    job = q.fetch_job(request_id)
    job_status = job.get_status()
    
    request_path = '../../../static/images/' + request_id + '.png'
    return render_template('index.html', request_path = request_path, job_status = job_status), 200

@app.route('/api/v1/queued_jobs')
def get_queued_jobs():
    queued_jobs = q.jobs

    return jsonify(queued_jobs), 200

@app.route('/api/v1/failed_jobs')
def get_failed_jobs():
    registry = q.failed_job_registry
    ids = registry.get_job_ids()

    results = []

    for id in ids:
        job = q.fetch_job(id)
        job_status = job.get_status()
        traceback = job.exc_info
        results.append({
            'job_id':  id,
            'job_status': job_status,
            'traceback': traceback
        })

    return jsonify(results), 200

if (__name__ == '__main__'):
    app.run(host='0.0.0.0', debug = True)