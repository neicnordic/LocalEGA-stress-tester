"""Base Test Design for DataEdge Scenario 4.

For this test we are aiming to download multiple unecrypted files.
The assumption is that the there are multiple tokens contains only one file
with the correct permissions,
and we can retrieve the ``file_{nb}_id`` via its corresponding token.
Scenario 4: Download an unencrypted file given a valid token.
"""

import sys
from ruamel.yaml import YAML
from locust import HttpLocust, TaskSet, task
from common import log_format

LOG = log_format('dataedge_scenario_4')


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
        if "token_1" not in self.config['scenario4'] and self.config['scenario4']['token_1'] is not None:
            LOG.error("Missing Token")
            sys.exit(1)
        else:
            self.token_1 = self.config['scenario4']['token_1']
            self.file_1_id = self.config['scenario4']['file_1_id']
            self.token_2 = self.config['scenario4']['token_2']
            self.file_2_id = self.config['scenario4']['file_2_id']
            self.ca = self.config['settings']['tls_ca_root_file']

    @task
    def get_query_1(self):
        """Test GET query endpoint."""
        url = f"/files/{self.file_1_id}?destinationFormat=plain"
        with self.client.get(url,
                             headers={'Autorization': f'Bearer {self.token_1}'},
                             verify=self.ca,
                             name='/files/[file_1_id]') as response:
            if response.status_code == 200:
                response.success()

    @task
    def get_query_2(self):
        """Test GET query endpoint."""
        url = f"/files/{self.file_2_id}?destinationFormat=plain"
        with self.client.get(url,
                             headers={'Autorization': f'Bearer {self.token_2}'},
                             verify=self.ca,
                             name='/files/[file_2_id]') as response:
            if response.status_code == 200:
                response.success()


class APITest(HttpLocust):
    """Test 4 DataEdge API.

    We need an HTTP Locust given the nature of the DataEdge API.
    """

    task_set = APIBehavior
    min_wait = 5000
    max_wait = 30000
