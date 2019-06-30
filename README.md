# ComputationalPhotographyProject
Docker setup is known to work on Debain 9.9. Almost surely won't work on Windows.
As the Spinnaker SDK requires Ubuntu 18.04, a Docker image had to be created.

# Steps
Some important steps form [other peoples projects](https://github.com/justinblaber/multi_pyspin) or the official `README.txt` in the SDK distribution, might be missing in the following list. Please read the official `README.txt`.

*   [Add your user](https://docs.docker.com/install/linux/linux-postinstall/) to the `docker` group to ensure, that you can run docker as non root
*   [check](https://unix.stackexchange.com/a/325972/40226) that your running X11 and not Wayland: `loginctl` to find your SESSION name (e.g. `2`) and run `loginctl show-session 2 -p Type`

*   Download the [Ubuntu18.04](https://flir.app.boxcn.net/v/SpinnakerSDK/folder/74729115388) folder of the SDK and extract it to the root of this project so that you have a directory called `Ubuntu18.04`.

*   To build the image form the Dockerfile run `./build.sh`

*   To run the image, run `./run.sh`. This script will start the container with the required flags.
