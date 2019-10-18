#!/bin/sh

[ -z "$TEST_TYPE" ] && echo "Specify Test type" && exit 1
[ -z "$TEST_NB" ] && echo "Specify Test nb" && exit 1
[ -z "$TESTED_ENDPOINT" ] && echo "Specify Tested endpoint" && exit 1

# Default values
CLIENTS=100
CLIENTS_SEC=10 # clients hatched at a certain rate per second
RUNTIME=20m

locust -f /locustfiles/"$TEST_TYPE"_test_"$TEST_NB".py \
       --host="$TESTED_ENDPOINT" \
       --no-web \
       --clients="$CLIENTS" \
       --hatch-rate="$CLIENTS_SEC" \
       --run-time="$RUNTIME" \
       --csv=/results/output_"$TEST_TYPE"_test_"$TEST_NB".csv
