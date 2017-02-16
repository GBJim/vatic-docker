#This is a fork of [Vatic-Docker ](https://github.com/jldowns/vatic-docker).
This version is focused on the **Vatic Offline Mode** which doesn't rely on the Amazon Mechanical Turk service
The following functions are added to turkic CLI
  1.turkic delete ASSIGNMENT  --> Delete a assignment(worker-video pair)
  2.turkic dump --image  --> Dump video frames into CatlTech Toolkit convention
  3.turkic dump --json  --> Dump annotations into JSON format. The structure has been modified to frame-based indexing
  4.turkic dump --split A:B --> Split mechanism that automatically divides data into multiple splits
  5.turkic dump --vbb   --> Dump annotations into vbb txt files that accepted by CalTech Toolkit
  6.turkic list --detail  --> List detailed hyperlinks-worker mapping of assignments and generate a user_map file.


# vatic-docker [![Build Status](https://travis-ci.org/jldowns/vatic-docker.svg?branch=master)](https://travis-ci.org/jldowns/vatic-docker)

Dockerfile and configuration files for using VATIC in a Docker container. Uses the VATIC software located at https://github.com/cvondrick/vatic

Right now everything runs in the same container. The parsed video frames reside on a volume on the host and therefore persist between runs. The direction below also explain how to dump the annotations to the volume. The only way to access the annotations outside the container is to dump them to a shared volume (like `/root/vatic/data`.) Emergency data retrieval procedures are outlined below.

## Running:
To annotate a video you must 1) extract the video into frames, and 2) publish the task, either locally or on Amazon Turk. I'll go over running annotations locally.

### To extract video:
Store your videos in `./data/videos_in`. The extracted frames will be sent to `./data/frames_in`. The example annotation script automatically runs the extraction script, so to after placing your video in the right spot you can skip to the next step. Note that after extraction the video is moved to `./data/videos_out` so that the system doesn't try to extract it again.

If you just want to extract the frames without running an annotation script, you can run
```
docker run -v "$PWD/data":/root/vatic/data jldowns/vatic-docker /root/vatic/extract.sh
```

### To annotate
Store your publishing script in `./annotation_scripts`. Run `vatic_up.sh <name of annotation script>`. This repository contains a script called `example.sh`, so to run it type
```
./vatic_up.sh example.sh
```

The example script does some things to streamline the process. It automatically calls the database/server startup script and opens a bash shell at the end. It also creates an HTML directory page, with a list of links to your published videos. Note that `annotation.sh`, running on the host, stored an IP:PORT in a file located in `./data/tmp`. Shared files are really the only way for the host machine and the guest process to communicate. I recommend basing your annotation scripts on the example script, at least the first time.

The last thing `example.sh` does is print out a URL that you can access that lists your published videos. That is a URL that is accessible from your host machine. Point your browser there and annotate away! You can even set up your machine to forward incoming traffic at the Docker container for collaborative annotations. Note that this is still "offline mode" since you're not using Amazon's services.

### To get your annotations out of the container

This is why the example script opens up a bash shell at the end; you have to do this step on the command line. Navigate to `/root/vatic` and type the following command

```
turkic dump currentvideo -o /root/vatic/data/output.txt
```
Where `currentvideo` is the ID from your annotation script and `ouput.txt` is the filename you want your annotations to be saved to. Look in your `./data` folder for the annotations.

## Ahh! I accidentally exited before dumping the annotations!
Find the container you just stopped by typing
```
docker ps -a
```
You can then restart and reattach the container and dump your data by typing
```
docker start $JOB
docker attach $JOB
```
where `$JOB` is the container ID. It's likely that the ID is still stored in the variable if you used the `vatic_up.sh` script.

## Caveats:
I have not tested the Amazon Mechanical Turk features.

## TODO:
- [x] Connect to server from host
- [x] Successfully annotate video and prove the process works.
- [x] Start annotating videos with only one command.
- [ ] More easily dump annotation data
- [X] Automated testing
