## LocalEGA Stress Tester Scripts

Load tool used for performing the tests is locust.io

Required: **Python 3.6+**

### Instructions

For installation run the following:
```
git clone https://github.com/NBISweden/LocalEGA-stress-tester
cd LocalEGA-stress-tester
pip install -r requirements.txt
# see if locust is installed
locust -h
cd stress_tests
```

#### Peforming the scenarios

Before performing the scenarios one needs to establish:
* Host address and Port for tested service;
* Number of clients and client spawned per second; e.g 100 users where there are 10 users spawned every second. In order to perform the evaluation this number can be increased or decreased per use case, as well as;
* Necessary configuration for the tests, based on scenario, has been added to:
  * Inbox tests: file, user and user private key in [stress_tests/inbox_config.yaml](stress_tests/inbox_config.yaml);
  * DataEdge tests: JWT Token for DataEdge, file to download [stress_tests/dataedge_config.yaml](stress_tests/dataedge_config.yaml);
* Set the name of the `csv` report in the command below under `<report_name>`.

```
locust -f locustfiles/test_dataedge_api.py \
       --host=http://ega-data-api:port \
       --no-web \
       --clients=100 \
       --hatch-rate=10 \
       --run-time=20m \
       --csv=<report_name>
```

### References

* https://docs.locust.io/en/latest/running-locust-without-web-ui.html