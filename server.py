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

def get_status_of_jobs(ids: list):
    results = []

    for id in ids:
        job = q.fetch_job(id)
        job_status = job.get_status()
        func_name = job.func_name
        enqueued_at = job.enqueued_at
        started_at = job.started_at
        ended_at = job.ended_at
        traceback = job.exc_info
        results.append({
            'job_id':  id,
            'job_status': job_status,
            'equneued_at': enqueued_at,
            'started_at': started_at,
            'ended_at': ended_at,
            'traceback': traceback
        })

    return results

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
        job = q.enqueue(networkgraph.NetworkGraph(url,1).draw_network_graph, request_id,
            job_timeout = '1h',
            job_id = request_id
        )
    else:
        return 'Could not instantiate networkgraph object.', 500

    return 'Processing in background. View result in about 10 minutes at: https://website-link-graph.herokuapp.com/api/v1/' + request_id, 200

@app.route('/api/v1/submit_url/<string:request_id>', methods = ['GET'])
def display_job(request_id):
    job = q.fetch_job(request_id)
    job_status = job.get_status()
    
    s3_url = 'https://website-link-graph.s3-us-west-1.amazonaws.com/'
    request_path = s3_url + request_id
    return render_template('index.html', request_path = request_path, job_status = job_status), 200

@app.route('/api/v1/queued_jobs')
def get_queued_jobs():
    queued_job_ids = q.job_ids

    results = get_status_of_jobs(queued_job_ids)

    return jsonify(results), 200

@app.route('/api/v1/failed_jobs')
def get_failed_jobs():
    registry = q.failed_job_registry
    failed_job_ids = registry.get_job_ids()

    results = get_status_of_jobs(failed_job_ids)

    return jsonify(results), 200

if (__name__ == '__main__'):
    app.run(host='0.0.0.0', debug = True)