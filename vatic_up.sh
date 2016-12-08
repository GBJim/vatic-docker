#!/bin/bash

ANNOTATION_SCRIPT="sample_pedestrian.sh"
HOST_ADDRESS_FILE="./data/tmp/host_address.txt"
mkdir -p ./data/tmp
echo "booting..." > $HOST_ADDRESS_FILE



JOB=$(\
docker run -ditp 8892:80 -v "$PWD/data":/root/vatic/data \
                 -v "$PWD/vatic":/root/vatic \
                 jldowns/vatic-docker /bin/bash -C /root/vatic/ascripts/$ANNOTATION_SCRIPT
    )

PORT=$(docker port $JOB 80 | awk -F: '{ print $2 }')
DHOSTIP=$(docker-machine ip default)

echo "---- Container attached at http://$DHOSTIP:$PORT/"
echo "$DHOSTIP:$PORT" > $HOST_ADDRESS_FILE
docker attach $JOB
