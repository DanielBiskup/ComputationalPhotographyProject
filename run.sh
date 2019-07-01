#!/usr/bin/env bash
containerId=app

xhost +local:root
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
docker run -ti \
  --mount type=bind,source="$(pwd)"/mount,target=/mount \
  -v $XSOCK:$XSOCK \
  -v $XAUTH:$XAUTH \
  -e XAUTHORITY=$XAUTH \
  --privileged \
  $containerId \
  bash
