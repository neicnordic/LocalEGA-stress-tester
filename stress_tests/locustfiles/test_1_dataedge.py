"""Base Test Design for DataEdge Scenario 1 and Scenario 5.

For this test we are aiming to download an unecrypted file.
The assumption is that the token contains only one file with the correct permissions,
and we can retrieve the ``file_id`` from the token.
Scenario 1: Download an unencrypted file given a valid token.
Scenario 5: Download an unencrypted large file given a valid token.
"""

import sys
from ruamel.yaml import YAML
from locust import HttpLocust, TaskSet, task
import logging

# Keeping it simple with the logging formatting
formatting = '[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s] (L:%(lineno)s) %(module)s | %(funcName)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=formatting)

LOG = logging.getLogger("dataedge_scenario_1")


class APIBehavior(TaskSet):
    """Test Tasks for DataEdge API."""

    def setup(self):
        """Test if the server is reachable."""
        with self.client.get("/", catch_response=True) as response:
            if response != 200:
                LOG.error("Data Edge API is not reachable")
                sys.exit(1)
        yaml = YAML(typ='safe')
        with open('../stress_tests/config.yaml', 'r') as stream:
            config = yaml.load(stream)
        if "token" not in config['localega'] and config['localega']['token'] is not None:
            LOG.error("Missing Token")
            sys.exit(1)

    @task
    def get_query(self):
        """Test GET query endpoint."""
        file_id = ''
        token = ''
        self.client.get(f"/files/{file_id}?destinationFormat=plain",
                        headers={'Autorization': f'Bearer {token}'},
                        name='/files/[file_id]')


class APITest(HttpLocust):
    """Test 1 DataEdge API.

    We need an HTTP Locust given the nature of the DataEdge API.
    """

    task_set = APIBehavior
    min_wait = 5000
    max_wait = 30000
