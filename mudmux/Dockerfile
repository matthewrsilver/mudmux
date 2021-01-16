FROM ubuntu:latest
LABEL description="A container for running tintin++ within mudmux, tmux-based MUD environment with scripts for playing the text-based RPG Medievia"

# Prepare for installs
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install bash wget gcc make

# Install tintin and its dependencies
RUN apt-get -y install zlibc zlib1g-dev libpcre3-dev
RUN wget https://sourceforge.net/projects/tintin/files/TinTin%2B%2B%20Source%20Code/2.02.0/tintin-2.02.00.tar.gz -P /tmp/ && tar -xvf /tmp/tintin*.tar.gz --directory /tmp/
WORKDIR /tmp/tt/src
RUN ./configure && make && make install

# Set up working environment
SHELL ["/bin/bash", "--login", "-c"]
WORKDIR /home/mudmux
