"""Base Test Design for DataEdge Scenario 5.

For this test we are aiming to download a large encrypted file.
The assumption is that the token contains only one file with the correct permissions,
and we can retrieve the ``file_id`` from the token.
Scenario 5: Download an encrypted large file given a valid token.
"""

import sys
from ruamel.yaml import YAML
from locust import HttpLocust, TaskSet, task
from common import log_format

LOG = log_format('dataedge_scenario_5')


class APIBehavior(TaskSet):
    """Test Tasks for DataEdge API."""

    def setup(self):
        """Test if the server is reachable."""
        with self.client.get("/", catch_response=True) as response:
            if response != 200:
                LOG.error("Data Edge API is not reachable")
                sys.exit(1)
        yaml = YAML(typ='safe')
        with open('../stress_tests/dataedge_config.yaml', 'r') as stream:
            self.config = yaml.load(stream)
        if "token" not in self.config['scenario5'] and self.config['scenario5']['token'] is not None:
            LOG.error("Missing Token")
            sys.exit(1)
        else:
            self.token = self.config['scenario5']['token']
            self.file_id = self.config['scenario5']['file_id']
            self.ca = self.config['settings']['tls_ca_root_file']

    @task
    def get_query(self):
        """Test GET query endpoint."""
        url = f"/files/{self.file_id}?destinationFormat=plain"
        with self.client.get(url,
                             headers={'Autorization': f'Bearer {self.token}'},
                             verify=self.ca,
                             name='/files/[file_id]') as response:
            if response.status_code == 200:
                response.success()


class APITest(HttpLocust):
    """Test 5 DataEdge API.

    We need an HTTP Locust given the nature of the DataEdge API.
    """

    task_set = APIBehavior
    # longer waiting times due to larger file
    min_wait = 30000
    max_wait = 90000
