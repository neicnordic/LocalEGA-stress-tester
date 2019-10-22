#!/bin/sh

# options for TEST_TYPE are inbox, dataedge, encdataedge
[ -z "$TEST_TYPE" ] && echo "Specify Test type." && exit 1

# values for TEST_NB are from 1 to 5
[ -z "$TEST_NB" ] && echo "Specify Test number." && exit 1

# TESTED_ENDPOINT should contain port as well
[ -z "$TESTED_ENDPOINT" ] && echo "Specify tested endpoint." && exit 1

# Default values
CLIENTS=100
CLIENTS_SEC=10 # clients hatched at a certain rate per second
RUNTIME=20m

# convert to lower case to be safe
TEST_TYPE_LO="$(echo "$TEST_TYPE" | tr '[:upper:]' '[:lower:]')"

locust -f /locustfiles/"$TEST_TYPE_LO"_test_"$TEST_NB".py \
       --host="$TESTED_ENDPOINT" \
       --no-web \
       --clients="$CLIENTS" \
       --hatch-rate="$CLIENTS_SEC" \
       --run-time="$RUNTIME" \
       --csv=/results/output_"$TEST_TYPE_LO"_test_"$TEST_NB".csv
