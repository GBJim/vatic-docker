#!/bin/bash

# Settings
#ID=currentvideo
USERS=(FOO BAR)
ANNOTATEDFRAMEPATH=/root/vatic/data/frames_in
TURKOPS="--offline --title HelloTurk!"
LABELS="person car"
HOST_ADDRESS_FILE=/root/vatic/data/tmp/host_address.txt

# Start database and server
/root/vatic/startup.sh

# Convert videos that need to be converted
/root/vatic/extract.sh

# Set up folders
mkdir -p $ANNOTATEDFRAMEPATH
cd /root/vatic

# start database
sudo /etc/init.d/mysql start

# load frames and publish. This will print out access URLs.
#turkic load $ID $ANNOTATEDFRAMEPATH $LABELS $TURKOPS
echo "Start to run the Python script"
python /root/vatic/load_publish.py

#for USER in $USERS[@] do
#	echo $USER
#	bash /root/vatic/load_video.sh $USER
#
# when we publish the videos, we'll also capture the address output and create
# links on a website. We sleep until the host system has time to record its IP address.
while [ `cat $HOST_ADDRESS_FILE` = "booting..." ]
do
    sleep 1
done
HOSTADDRESS=`cat $HOST_ADDRESS_FILE`
mkdir -p /root/vatic/public/directory

# replace the 'localhost' of the output to the host's address, and format it into
# a series of html links. Save this at the /directory page in the website.
{ turkic publish --offline |\
  tee /dev/fd/3 | sed "s/http/<a href='http/" |\
                  sed "s/offline/offline'> Video Segment <\/a><br>/" |\
                  sed "s/localhost/$HOSTADDRESS/" >| /root/vatic/public/directory/index.html; } 3>&1


# open up a bash shell on the server

echo "Please go to http://$HOSTADDRESS/directory for links."

/bin/bash
