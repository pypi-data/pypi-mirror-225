import atexit
import signal
import sys
import threading
from os import getenv

from llm_monitor.schema.transaction import TransactionRecord, TransactionRecordBatch
from llm_monitor.utils.api_client import ApiClient

LOOP_INTERVAL = 1
BATCH_SEND_INTERVAL = 10
MAX_BATCH_SIZE = 20
BATCH = []

BATCHING_DISABLED = getenv("LLMM_BATCHING_DISABLED") in ["true", "True", True]

client: ApiClient


def initialize_api_client(project_name: str):
    global client
    client = ApiClient(project_name=project_name)


# This method is called by handlers/wrappers to add a new
# record to the send queue
def add_record_to_batch(record: TransactionRecord) -> None:
    global BATCH
    BATCH.append(record)
    # If we've hit our max BATCH size, don't wait for the next interval
    if (len(BATCH) == MAX_BATCH_SIZE) or BATCHING_DISABLED:
        _send_batch()


def _send_batch() -> None:
    global BATCH
    if len(BATCH) > 0:
        # print(f"Sending batch of {len(BATCH)} records to the Galileo API")
        transaction_batch = TransactionRecordBatch(records=BATCH)
        client.ingest_batch(transaction_batch)
        BATCH = []


def _signal_handler(signum, frame):
    global job
    job.stop()
    sys.exit()


class Job(threading.Thread):
    def __init__(self, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = True
        self.stopped = threading.Event()
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

        # Send whatever is left in the queue before exiting
        atexit.register(_send_batch)

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        elapsed_time = 0
        while not self.stopped.wait(LOOP_INTERVAL):
            if elapsed_time >= BATCH_SEND_INTERVAL:
                self.execute(*self.args, **self.kwargs)
                elapsed_time = 0
            else:
                elapsed_time = elapsed_time + LOOP_INTERVAL


if not BATCHING_DISABLED:
    # Add signal handlers to make sure we terminate the send_batch job thread
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    # Create the send_batch timed job and start it
    job = Job(execute=_send_batch)
    job.start()
