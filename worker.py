import os

import redis
from rq import Worker, Queue, Connection

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'./src'))
import networkgraph 

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()