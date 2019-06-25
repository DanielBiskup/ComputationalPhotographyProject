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
CMD ["/usr/bin/xeyes"]
