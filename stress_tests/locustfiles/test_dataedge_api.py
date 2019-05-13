import sys
from os import environ
from locust import HttpLocust, TaskSet, task
import logging

# Keeping it simple with the logging formatting

formatting = '[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s] (L:%(lineno)s) %(module)s | %(funcName)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=formatting)

LOG = logging.getLogger("test_dataedge")


class APIBehavior(TaskSet):
    """Test Tasks for DataEdge API."""

    def setup(self):
        """Test if the server is reachable."""
        with self.client.get("/", catch_response=True) as response:
            # TO DO Double check if this is the right way to do this
            if response != 200:
                LOG.error("Data Edge API is not reachable")
                sys.exit(1)
        if "TOKEN" not in environ:
            LOG.error("Missing Token")
            sys.exit(1)

    @task
    def get_token(self):
        """Test the info endpoint.

        The only endpoint that has some sort of caching.
        """
        self.client.get("/")

    @task
    def get_query(self):
        """Test GET query endpoint."""
        file_id = ''
        token = ''
        self.client.get(f"/files/{file_id}?destinationFormat=plain",
                        headers={'Autorization': f'Bearer {token}'},
                        name='/files/[file_id]')


class APITest(HttpLocust):
    """Test DataEdge API."""

    task_set = APIBehavior
    min_wait = 5000
    max_wait = 30000
