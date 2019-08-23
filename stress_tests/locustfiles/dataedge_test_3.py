"""Base Test Design for DataEdge Scenario 3.

For this test we are aiming to download multiple unecrypted files.
The assumption is that the token contains only one file with the correct permissions,
and we can retrieve the ``file_{nb}_id`` from the token.
Scenario 3: Download multiple unencrypted files given a valid token.
"""

import sys
from ruamel.yaml import YAML
from locust import HttpLocust, TaskSet, task
from common import log_format

LOG = log_format('dataedge_scenario_3')


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
        if "token" not in self.config['scenario3'] and self.config['scenario3']['token'] is not None:
            LOG.error("Missing Token")
            sys.exit(1)
        else:
            self.token = self.config['scenario3']['token']
            self.file_1_id = self.config['scenario3']['file_1_id']
            self.file_2_id = self.config['scenario3']['file_2_id']
            self.file_3_id = self.config['scenario3']['file_3_id']
            self.file_4_id = self.config['scenario3']['file_4_id']
            self.file_5_id = self.config['scenario3']['file_5_id']
            self.ca = self.config['settings']['tls_ca_root_file']

    @task
    def get_query_1(self):
        """Test GET query endpoint file 1."""
        url = f"/files/{self.file_1_id}?destinationFormat=plain"
        with self.client.get(url,
                             headers={'Autorization': f'Bearer {self.token}'},
                             verify=self.ca,
                             name='/files/[file_1_id]') as response:
            if response.status_code == 200:
                response.success()

    @task
    def get_query_2(self):
        """Test GET query endpoint file 2."""
        url = f"/files/{self.file_2_id}?destinationFormat=plain"
        with self.client.get(url,
                             headers={'Autorization': f'Bearer {self.token}'},
                             verify=self.ca,
                             name='/files/[file_2_id]') as response:
            if response.status_code == 200:
                response.success()

    @task
    def get_query_3(self):
        """Test GET query endpoint file 3."""
        url = f"/files/{self.file_3_id}?destinationFormat=plain"
        with self.client.get(url,
                             headers={'Autorization': f'Bearer {self.token}'},
                             verify=self.ca,
                             name='/files/[file_3_id]') as response:
            if response.status_code == 200:
                response.success()

    @task
    def get_query_4(self):
        """Test GET query endpoint file 4."""
        url = f"/files/{self.file_4_id}?destinationFormat=plain"
        with self.client.get(url,
                             headers={'Autorization': f'Bearer {self.token}'},
                             verify=self.ca,
                             name='/files/[file_4_id]') as response:
            if response.status_code == 200:
                response.success()

    @task
    def get_query_5(self):
        """Test GET query endpoint file 5."""
        url = f"/files/{self.file_5_id}?destinationFormat=plain"
        with self.client.get(url,
                             headers={'Autorization': f'Bearer {self.token}'},
                             verify=self.ca,
                             name='/files/[file_id]') as response:
            if response.status_code == 200:
                response.success()


class APITest(HttpLocust):
    """Test 3 DataEdge API.

    We need an HTTP Locust given the nature of the DataEdge API.
    """

    task_set = APIBehavior
    min_wait = 5000
    max_wait = 30000
