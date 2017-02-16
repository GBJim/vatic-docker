#!/bin/bash
NAME="vatic"

if [ "$(docker ps -aq -f name=$NAME)" ]; then

    if [ "$(docker ps -aq -f status=exited -f name=$NAME)" ]; then
        # Start the exited container
        echo "The exited continer $NAME exists"
        docker start $NAME
    fi

    echo "The continer $NAME is already running"


else
  echo "Start continer from image"
  # Start from image
  ANNOTATION_SCRIPT="sample_pedestrian.sh"
  HOST_ADDRESS_FILE="./data/tmp/host_address.txt"
  mkdir -p ./data/tmp
  echo "booting..." > $HOST_ADDRESS_FILE



  JOB=$(\
  docker run -ditp 8892:80 -v "$PWD/data":/root/vatic/data \
                   -v "$PWD/vatic":/root/vatic \
                   --name $NAME\
                   jldowns/vatic-docker /bin/bash -C /root/vatic/ascripts/$ANNOTATION_SCRIPT

      )

  PORT=$(docker port $JOB 80 | awk -F: '{ print $2 }')


  echo "---- Container attached at http://localhost:$PORT/"
  echo "$DHOSTIP:$PORT" > $HOST_ADDRESS_FILE
fi



#Attach continer
docker attach $NAME
