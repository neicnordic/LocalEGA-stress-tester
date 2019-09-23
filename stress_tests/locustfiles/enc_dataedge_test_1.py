"""Base Test Design for DataEdge Scenario 1.

For this test we are aiming to download an encrypted file.
The assumption is that the token contains only one file with the correct permissions,
and we can retrieve the ``file_id`` from the token.
Scenario 1: Download an encrypted file given a valid token.
"""

import sys
from ruamel.yaml import YAML
from locust import HttpLocust, TaskSet, task
from common import log_format

LOG = log_format('encrypted_dataedge_scenario_1')


class APIBehavior(TaskSet):
    """Test Tasks for DataEdge API."""

    def setup(self):
        """Test if the server is reachable."""
        with self.client.get("/", catch_response=True) as response:
            if response != 200:
                LOG.error("Data Edge API is not reachable")
                sys.exit(1)
        yaml = YAML(typ='safe')
        with open('../stress_tests/enc_dataedge_config.yaml', 'r') as stream:
            self.config = yaml.load(stream)
        if "token" not in self.config['scenario1'] and self.config['scenario1']['token'] is not None:
            LOG.error("Missing Token")
            sys.exit(1)
        else:
            self.token = self.config['scenario1']['token']
            self.file_id = self.config['scenario1']['file_id']
            self.format = self.config['scenario1']['encrypted']['format']
            self.key = self.config['scenario1']['encrypted']['key']
            self.iv = self.config['scenario1']['encrypted']['iv']
            self.ca = self.config['settings']['tls_ca_root_file']

    @task
    def get_query(self):
        """Test GET query endpoint."""
        url = f"/files/{self.file_id}?destinationFormat={self.format}&destinationKey={self.key}&destinationIV={self.iv}"
        with self.client.get(url,
                             headers={'Authorization': f'Bearer {self.token}'},
                             verify=self.ca,
                             name='/files/[file_id]') as response:
            if response.status_code == 200:
                response.success()


class APITest(HttpLocust):
    """Test 1 Encrypted file download via DataEdge API.

    We need an HTTP Locust given the nature of the DataEdge API.
    """

    task_set = APIBehavior
    min_wait = 5000
    max_wait = 30000
