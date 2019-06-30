[FLIR SDK](https://flir.app.boxcn.net/v/SpinnakerSDK)

[multi_pyspin - A simple multi camera library using PySpin](https://github.com/justinblaber/multi_pyspin)

# Dockerfile:
https://docs.docker.com/get-started/part2/
http://phase2.github.io/devtools/common-tasks/ssh-into-a-container/


```bash
# Build a Dockerfile (generates an image) with name `myApp`:
docker build --tag=myapp:v1 .

# List existing images:
docker image ls

# Run docker image:
docker run myapp:v1

# Run docker image with interactive tty and bash:
docker run --interactive --tty myapp:v1 bash
```

[Name your own containers](https://stackoverflow.com/questions/25230812/when-to-use-dockers-container-name) with `--name` when you use `docker run`.

## Running GUI application in a docker container
https://medium.com/@SaravSun/running-gui-applications-inside-docker-containers-83d65c0db110

Flags to run docker with:

  * share the Host’s XServer with the Container by creating a volume `--volume="$HOME/.Xauthority:/root/.Xauthority:rw"`
  * share the Host’s DISPLAY environment variable to the Container `--env="DISPLAY"`
  * run container with host network driver with `--net=host`

# The workiung solution to X-Forwarding on Docker
https://stackoverflow.com/questions/16296753/can-you-run-gui-applications-in-a-docker-container

Use the `Dockerfile` given here:
```
# This install is for ubuntu 18.04 and python 3.6
FROM ubuntu:18.04

# Disable interactive dialogue with dpkg
ENV DEBIAN_FRONTEND noninteractive

# Disable python user site
ENV PYTHONNOUSERSITE 1

# Update
RUN apt-get -y update

# Install python/pip
RUN apt-get -y install python3 && \
    apt-get -y install python3-pip

# Install git
RUN apt-get -y install git

# create app directory
RUN mkdir /app

# Set the working directory to /app
WORKDIR /app

# Copy the SDK zip
COPY ./Ubuntu18.04/ /app

# Install SpinnakerSDK
RUN cd /app && \
    tar xvfz spinnaker-1.23.0.27-amd64-Ubuntu18.04-pkg.tar.gz && \
    cd spinnaker-1.23.0.27-amd64 && \
    apt-get -y install sudo && \
    apt-get -y install libusb-1.0-0

# RUN printf 'y\nn\n' | sh install_spinnaker.sh

RUN apt-get install -y x11-apps
ENV DISPLAY :0
CMD ["/usr/bin/xeyes"]
```

# Error caused by later lines of the `install_spinnaker.sh`
I have to delete some lines in the script which I don't need, because otherwise
the script would otherwise fail with some error.
```bash
sed -i '50,101d' install_spinnaker.sh  
```

# How it works
build it with
```bash
docker build --tag=myapp:v1 .
```

Run with [x11 Forwarding](https://stackoverflow.com/a/25280523/1510873) is [possible](http://wiki.ros.org/docker/Tutorials/GUI#The_simple_way) as follwos:
```bash
xhost +local:root
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
containerId=app
docker run -ti -v $XSOCK:$XSOCK -v $XAUTH:$XAUTH -e XAUTHORITY=$XAUTH $containerId bash
```
when your done with your work you should remove the permission above again, for
security reasons:
```bash
xhost -local:root
```

Also run with the
[`--privileged` flag](https://stackoverflow.com/a/55198696/1510873),
so that it can use the USB devices, in this case the camera:
```bash
docker run -ti --privileged ubuntu bash
```

deps:
* `apt install libgl1-mesa-glx` [here](https://github.com/ContinuumIO/docker-images/issues/49#issuecomment-302152488)
* `apt -y install libqt5x11extras5` [here](https://askubuntu.com/a/902774/163596)
