Data API Testing Specs
======================

Testing environments
--------------------

Testing environments below should test with both types of backend storage S3 and POSIX.
A JWT Token along with its corresponding Public Key will need to be set up for the testing environment,

1. DataEdge as part of the LocalEGA + Data API Stack:

  - We have all the ingestion and outgestion components running.

2. DataEdge as part the Data API stack:

  - in case we just want to test the performance with no hassle of setting up the full stack

Endpoints are described at: https://github.com/EGA-archive/ega-data-api/tree/master/mock-services/openapi/dataedge
and we will be focusing on the /files endpoint with both encrypted and decrypted format.

Maximum expected load
---------------------

.. note:: this would be the success criteria, by which we make sure that under such a load the system recovers easily.

In order to determine the expected user load, or more precisely the system limits we are
going to perform an exploratory performance tests at this stage.

 e.g. x concurrent users downloading files without the service crashing or becoming unusable.
 e.g. 1000/10000 users that download simultaneously.
 (we should also establish some file sizes e.g. 100Mb, 1Gb or 10Gb for the expected load)


Metrics
-------

1. Average operation response time - successful/erroneous operations
2. Total number of transactions per second - total successful, total erroneous operations in a second
3. Response time under heavy load - do we experience any throttling under heavy load

Testing Scenarios
-----------------

The scenarios will consistent of two stages:
Exploratory Stage - where we try to identify the limits of the system, based on different setups
- meaning try to first perform the test in local environment then move to a deployed environment,
but without any scaling enabled. With this we will be able to figure out the limits
Perform the tests but with different scaling strategies - vertical or horizontal.

Hypothesis
~~~~~~~~~~

We should be able to do multiple types of operations, at the same time with multiple users. For this purpose we must considers scenarios that overload the system such as:

1. Load testing - increase user load over a period of time

  - 10 users try to download a file
  - 100 users try to download a file
  - 1000 users try to download a file

2. Test 100 users trying to download 1Gb file at the same time

3. Test different scenarios with the DataEdge API endpoint with e.g. 100 users

  - download a file that exists
  - download a file that does not exist
  - try different parameters of the DataEdge API endpoints

Scenarios Template
~~~~~~~~~~~~~~~~~~

1. User tries the endpoints

    - ``/files/{file_id}?destinationFormat=plain``
    - ``/files/{file_id}?destinationFormat={aes,crypt4gh}&destinationKey={key}&destinationIV={iv}``
    - User provides appropriate headers with JWT token
2. User waits for download to finish.

+-----------------------------------------------+-------------------------------------------+
| Scenario 1                                    | Scenario 2                                |
+-----------------------------------------------+-------------------------------------------+
| Token with correct permissions                | token with no data access                 |
+-----------------------------------------------+-------------------------------------------+
| Download Decrypted file                       | Download a file user does not have access |
+-----------------------------------------------+-------------------------------------------+
| Response should be 200 in given time interval | Should return the 403 error               |
+-----------------------------------------------+-------------------------------------------+


+----------------------------------------+------------------------------------------+
| Scenario 3                             | Scenario 4                               |
+----------------------------------------+------------------------------------------+
| Provide token with correct permissions | Multiple tokens with correct permissions |
+----------------------------------------+------------------------------------------+
| Download multiple decrypted files      | Download multiple decrypted files        |
+----------------------------------------+------------------------------------------+
| Response is 200 in time interval       | Response is 200 in time interval         |
+----------------------------------------+------------------------------------------+

.. note:: For scenario 3 and scenario 4 response should be ``200`` for all files.


+---------------------------------------------------------------------------------------+
| Scenario 5                                                                            |
+---------------------------------------------------------------------------------------+
| Token with correct permissions                                                        |
+---------------------------------------------------------------------------------------+
| Download decrypted big file(s)                                                        |
+---------------------------------------------------------------------------------------+
| Response should be 200 in given time interval and the connection should be kept alive |
+---------------------------------------------------------------------------------------+

Tools
-----

Custom build Locust http://locust.io/ files for each scenario, or we might be able to group them together.
We will have to add functionality so that we can measure the speed.


