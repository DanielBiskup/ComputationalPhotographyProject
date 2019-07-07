#!/usr/bin/env bash

# Set the usbfs_memory_mb
# As mentioned here:
#    https://github.com/nimble00/PTGREY-cameras-with-python/issues/2#issuecomment-501676938
#    https://www.flir.com/support-center/iis/machine-vision/application-note/understanding-usbfs-on-linux/
sudo sh -c 'echo 1000 > /sys/module/usbcore/parameters/usbfs_memory_mb'

# Run the container with the required flags for X11 forwarding.
containerId=app
xhost +local:root
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
docker run -ti \
  --mount type=bind,source="$(pwd)"/src,target=/src \
  -v $XSOCK:$XSOCK \
  -v $XAUTH:$XAUTH \
  -e XAUTHORITY=$XAUTH \
  --privileged \
  $containerId \
  bash
