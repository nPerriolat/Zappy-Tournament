#!/bin/bash

if [[ $1 == "debug" ]]; then
    echo "Debug mode"
    bashing="--entrypoint /bin/bash"
fi

xhost +local:docker
docker run --network none --device /dev/dri/ -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -it --rm $bashing zappy_container
xhost -local:docker
