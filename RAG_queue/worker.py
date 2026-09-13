# worker.py

from rq import SimpleWorker
from .client.rd_client import queue

if __name__ == "__main__":
    worker = SimpleWorker([queue])
    worker.work()