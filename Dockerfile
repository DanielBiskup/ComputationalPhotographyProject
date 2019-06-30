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

RUN apt-get install -y x11-apps
ENV DISPLAY :0

# Spinnacker setup:
## 1. Dependency Installation
RUN sudo apt-get -y install \
        libavcodec57 \
        libavformat57 \
        libswscale4 \
        libswresample2 \
        libavutil55 \
        libusb-1.0-0 \
        libgtkmm-2.4-dev

## 2. USB RELATED NOTES

## 3. SPINNAKER INSTALLATION
# RUN printf 'y\nn\nn\n' | sh install_spinnaker.sh

RUN cd /app/spinnaker-1.23.0.27-amd64 && \
    sed -i '50,101d' install_spinnaker.sh && \
    printf 'y\nn\n' | sh install_spinnaker.sh

## Install some dependencies for the SpinView_QT:
RUN apt-get -y install libgl1-mesa-glx # https://github.com/ContinuumIO/docker-images/issues/49#issuecomment-302152488
RUN apt-get -y install libqt5x11extras5 # https://askubuntu.com/a/902774/163596

CMD ["/usr/bin/xeyes"]
