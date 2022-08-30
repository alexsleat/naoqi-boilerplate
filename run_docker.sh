. docker_config

docker run \
    -it --privileged \
    -v /dev/bus/usb:/dev/bus/usb \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    -v $(pwd)/code:/home/user/code \
    --name $CONTAINER_NAME  \
    $DOCKER_NAME bash