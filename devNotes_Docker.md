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

## Using `bind` vs `mount`?
We want to have access to a directory on our system. That's a job for `bind` (as pointed out [here](Bind mounts have been around since the early days of Docker. Bind mounts have limited functionality compared to volumes. When you use a bind mount, a file or directory on the host machine is mounted into a container. The file or directory is referenced by its full or relative path on the host machine. By contrast, when you use a volume, a new directory is created within Docker’s storage directory on the host machine, and Docker manages that directory’s contents.).
`mount` on the other hand would create a new directory on the host which then would be managed by Docker.

To make the the folder `mount` from the projects root directory accessible in the container, we need to therefore mount it with:
```
--mount type=bind,source="$(pwd)"/mount,target=/mount
```
This flag was added to the `run.sh` script. It's assumed that `run.sh` will be run with the projects root as the current working directory.

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

# Only one of the two Grasshopper3 Cameras working. Gray camera also not working

## Fixing the Color Camera
### Get firmware:
Our Grasshopper3 camera is of model **GS3-U3-23S6C-C**.

Or other SDK, i.e. FlyCap

* [Support page on 'Grasshopper3 Firmware'](https://www.flir.com/support/?query=Grasshopper3+Firmware)
* ['Box' directory firmware for all versions of 'Grasshopper3 USB3 Firmware'](https://flir.app.boxcn.net/s/32307vvdezwgu27g6eojf5qw8z6mmndt)
* [Firmware download for our particular Grasshopper3 version, i.e. `gs3-u3-23s6m-c`](https://flir.app.boxcn.net/s/32307vvdezwgu27g6eojf5qw8z6mmndt/file/418659834016)

The `mount` directory in the projects root is bind-mounted into the container. Thus we can copy the Firmware update there and apply it from inside the container with:
```
cd /mount/FIRMWARE/GS3-U3-2.30.3.0-23S6
SpinUpdateConsole -R16010860 GS3-U3-2.30.3.0-23S6.ez2
```
I tried just now, but it doesn't change anything... The output of the SpinUpdateConsole doesn't tell me much.
```
root@e36f53651a91:/mount/FIRMWARE/GS3-U3-2.30.3.0-23S6# SpinUpdateConsole -R16010860 GS3-U3-2.30.3.0-23S6.ez2
Reading firmware file:
Updater Initialization...
Get USB cameras...
Get GigE cameras...
Number of FLIR camera(s) discovered: 1
FF010000: skipping
FFF80000: wrong timestamp
FFFE0000: wrong timestamp
FF080000: skipping
FFF90000: wrong timestamp
FFFD0000: wrong timestamp
FFFFD000: wrong version
FFF80000: erase SA00: FFF80000..FFF83FFF
FFF80000: erase SA01: FFF84000..FFF87FFF
FFF80000: erase SA02: FFF88000..FFF8BFFF
FFFE0000: erase SA24: FFFE0000..FFFE3FFF
FFFE0000: erase SA25: FFFE4000..FFFE7FFF
FFFE0000: erase SA26: FFFE8000..FFFEBFFF
FFF90000: erase SA04: FFF90000..FFF93FFF
FFF90000: erase SA05: FFF94000..FFF97FFF
FFF90000: erase SA06: FFF98000..FFF9BFFF
FFF90000: erase SA07: FFF9C000..FFF9FFFF
FFF90000: erase SA08: FFFA0000..FFFA3FFF
FFF90000: erase SA09: FFFA4000..FFFA7FFF
FFF90000: erase SA10: FFFA8000..FFFABFFF
FFF90000: erase SA11: FFFAC000..FFFAFFFF
FFF90000: erase SA12: FFFB0000..FFFB3FFF
FFFD0000: erase SA20: FFFD0000..FFFD3FFF
FFFD0000: erase SA21: FFFD4000..FFFD7FFF
FFFD0000: erase SA22: FFFD8000..FFFDBFFF
FFFFD000: erase SA35: FFFFD000..FFFFDFFF
HAL Updater Complete
```

Spinview shows for A:
Serial Number: 16010805
FW:v2.25.3.00 FPGA:v2

Spinview shows for B:
Serial Number: 16010860
FW:v2.30.3.00 FPGA:v2.02

# Q:
Buildung the Dockerfile fails with:
```
E: Failed to fetch http://archive.ubuntu.com/ubuntu/pool/main/libd/libdrm/libdrm-common_2.4.95-1~18.04.1_all.deb  404  Not Found [IP: 91.189.91.26 80]
```
what's most likely the problem, and how to fix it?
# A:
https://stackoverflow.com/a/37727984/1510873
You need to add `apt-get -y update` as the first command in every `RUN` block which runs `apt-get -y install`. That's because of Dockers build caching.
