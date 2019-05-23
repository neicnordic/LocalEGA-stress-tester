"""Base Test Design for DataEdge Scenario 1 and Scenario 5.

For this test we are aiming to download an ecrypted file.
The assumption is that the token contains only one file with the correct permissions,
and we can retrieve the ``file_id`` from the token.
Scenario 1: Download an encrypted file given a valid token.
Scenario 5: Download an encrypted large file given a valid token.
"""

import sys
from ruamel.yaml import YAML
from locust import HttpLocust, TaskSet, task
from common import log_format

LOG = log_format('dataedge_scenario_2')


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
            self.config = yaml.load(stream)
        if "token" not in self.config['scenario2'] and self.config['scenario2']['token'] is not None:
            LOG.error("Missing Token")
            sys.exit(1)
        else:
            self.token = self.config['scenario1']['token']
            self.file_id = self.config['scenario1']['file_id']
            self.format = self.config['scenario1']['encrypted']['format']
            self.key = self.config['scenario1']['encrypted']['key']
            self.iv = self.config['scenario1']['encrypted']['iv']

    @task
    def get_query(self):
        """Test GET query endpoint."""
        self.client.get(f"/files/{self.file_id}?destinationFormat={self.format}&destinationKey={self.key}&destinationIV={self.iv}",
                        headers={'Autorization': f'Bearer {self.token}'},
                        name='/files/[file_id]')


class APITest(HttpLocust):
    """Test 2 DataEdge API.

    We need an HTTP Locust given the nature of the DataEdge API.
    """

    task_set = APIBehavior
    min_wait = 5000
    max_wait = 30000
