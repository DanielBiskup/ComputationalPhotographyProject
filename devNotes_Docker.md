Resources used here:

*   [FLIR SDK](https://flir.app.boxcn.net/v/SpinnakerSDK)
*   [multi_pyspin - A simple multi camera library using PySpin](https://github.com/justinblaber/multi_pyspin)

# Building and running the Docker image
## General things
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

# X11 Forwading so that you can run GUI applications in your container
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
And in the Dockerfile `ENV DISPLAY :0` indicates which display to use.

## Give container access to the USB camera of the host
Also run with the
[`--privileged` flag](https://stackoverflow.com/a/55198696/1510873),
so that it can use the USB devices, in this case the camera:
```bash
docker run -ti --privileged ubuntu bash
```

**Note** however, that the camera needs to be plugged in before starting the container.

# Some explaination of what the Dockerfile does

## Install some dependencies `SpinView` requires
*   `apt install libgl1-mesa-glx` [here](https://github.com/ContinuumIO/docker-images/issues/49#issuecomment-302152488)
*   `apt -y install libqt5x11extras5` [here](https://askubuntu.com/a/902774/163596)

## Remove some lines to prevent error caused by later lines of the `install_spinnaker.sh`
I have to delete some lines in the script which I don't need, because otherwise
the script would otherwise fail with some error.
```bash
sed -i '50,101d' install_spinnaker.sh  
```


# Get firmware:
flir gs3-u3-23s6m-c firmware
  / ms6-c

Or other SDK, i.e. FlyCap
