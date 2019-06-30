#!/usr/bin/env bash
xhost +local:root
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
containerId=app
docker run -ti \
  -v $XSOCK:$XSOCK \
  -v $XAUTH:$XAUTH \
  -e XAUTHORITY=$XAUTH \
  --privileged \
  $containerId \
  bash
