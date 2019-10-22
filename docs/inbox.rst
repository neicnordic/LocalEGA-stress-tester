Inbox Testing Specs
===================

Testing environments
--------------------

Testing environments below should test with both types of backend storage S3 and POSIX.

1. Isolated Inbox - A scenario where we focus exclusively on the inbox

  - For the test we mock the Inbox dependencies such as MQ and CEGA-users
  - Makes more sense in a scenario for Load Testing

2. Inbox as part of the Ingestion Stack:

  - We have all the ingestion components running.

Maximum expected load
---------------------

.. note:: this would be the success criteria, by which we make sure that under such a load the system recovers easily.

In order to determine the expected user load, or more precisely the system limits we are going
to perform an exploratory performance tests in this stage.

 e.g. x concurrent users uploading files without the services crashing or becoming unusable.
 e.g. 1000/10000 users that upload (or perform an operation with inbox) simultaneously.
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
Perform the tests but with different scaling strategies - vertical or horizontal .

Hypothesis
~~~~~~~~~~
We should be able to do multiple types of operations, at the same time with multiple users.
In the exploratory phase we will establish the limits of the system and to what degree of expected load we can stress the system, and still maintain functionality. For this purpose we must considers scenarios that overload the system such as:

1. Load testing - increase user load over a period of time

  - 10 users try to submit a file
  - 100 users try to submit a file
  - 1000 users try to submit a file

2. Test 100 users trying to upload 1Gb file at the same time

3. Test different operations in the inbox with e.g. 100 users

  - upload (might already be covered by the scenarios above)
  - remove (maybe try to delete the same file)
  - rename

Scenarios Template
~~~~~~~~~~~~~~~~~~

1. User enters inbox

    - User selects an encrypted file
2. User does operation with a file or multiple files (upload, rename, remove)
3. Finishes operation, e.g. exit inbox

    - Enters the inbox again and repeats step 2 and 3.

+------------+------------+------------+------------+------------+
| Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4 | Scenario 5 |
+------------+------------+------------+------------+------------+
| Connect    | Connect    | Connect    | Connect    | Connect    |
+------------+------------+------------+------------+------------+
| Upload     | Upload     | Upload     | Upload     | Upload     |
+------------+------------+------------+------------+------------+
| Disconnect | Disconnect | Rename     | Rename     | Disconnect |
+------------+------------+------------+------------+------------+
|            | Reconnect  | Disconnect | Remove     | Reconnect  |
+------------+------------+------------+------------+------------+
|            | Rename     |            | Disconnect | Rename     |
+------------+------------+------------+------------+------------+
|            | Disconnect |            |            | Disconnect |
+------------+------------+------------+------------+------------+
|            |            |            |            | Reconnect  |
+------------+------------+------------+------------+------------+
|            |            |            |            | Remove     |
+------------+------------+------------+------------+------------+
|            |            |            |            | Disconnect |
+------------+------------+------------+------------+------------+

Tools
-----

1. Build our own:
Custom build Locust http://locust.io/ files for each scenario.
It seems we are able to use locust for this purpose from initial tests.
As this will be used in Data API performance testing, make sense to use the same tool.
To Be Establish what data we can extract, based on this custom tool.
We will have to add functionality so that we can measure the speed.
2. Use JMeter - seems the most appropriate one

Further Reading
---------------

* http://tryqa.com/what-is-stress-testing-in-software/
* https://www.blazemeter.com/blog/load-testing-ftp-and-sftp-servers-using-jmeter
