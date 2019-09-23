"""Base Test Design for DataEdge Scenario 2.

For this test we are aiming to download an unecrypted file.
The assumption is that the token does not contains only the correct permissions,
and we will receive a 403 from the Dataedge Service.
Scenario 2: Download an unencrypted file given a token with no data access.
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
        with open('../stress_tests/dataedge_config.yaml', 'r') as stream:
            self.config = yaml.load(stream)
        if "token" not in self.config['scenario2'] and self.config['scenario2']['token'] is not None:
            LOG.error("Missing Token")
            sys.exit(1)
        else:
            self.token = self.config['scenario2']['token']
            self.file_id = self.config['scenario2']['file_id']
            self.ca = self.config['settings']['tls_ca_root_file']

    @task
    def get_query(self):
        """Test GET query endpoint."""
        url = f"/files/{self.file_id}?destinationFormat=plain"
        with self.client.get(url,
                             headers={'Authorization': f'Bearer {self.token}'},
                             verify=self.ca,
                             name='/files/[file_id]') as response:
            if response.status_code == 403:
                response.success()


class APITest(HttpLocust):
    """Test 2 DataEdge API.

    We need an HTTP Locust given the nature of the DataEdge API.
    """

    task_set = APIBehavior
    min_wait = 5000
    max_wait = 30000
