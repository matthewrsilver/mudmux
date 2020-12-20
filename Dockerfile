FROM ubuntu:latest
LABEL description="mudmux tintin-based medievia environment"

# Prepare for installs
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install bash wget gcc make

# Install tintin and its dependencies
RUN apt-get -y install zlibc zlib1g-dev libpcre3-dev
RUN wget https://sourceforge.net/projects/tintin/files/TinTin%2B%2B%20Source%20Code/2.01.8/tintin-2.01.8.tar.gz -P /tmp/ && tar -xvf /tmp/tintin*.tar.gz --directory /tmp/
WORKDIR /tmp/tt/src
RUN ./configure && make && make install

# Set up working environment
SHELL ["/bin/bash", "--login", "-c"]
ENV PATH="$PATH:/home/mudmux/bin"
WORKDIR /home/mudmux
