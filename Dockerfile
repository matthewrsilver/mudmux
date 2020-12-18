FROM alpine:latest
LABEL description="muxmed tintin-based medievia environment"

# Prepare for installs
RUN apk update && apk upgrade
RUN apk add alpine-sdk bash

# Install tintin and its dependencies
RUN apk add zlib-dev pcre-dev
RUN wget https://sourceforge.net/projects/tintin/files/TinTin%2B%2B%20Source%20Code/2.01.8/tintin-2.01.8.tar.gz -P /tmp/ && tar -xvf /tmp/tintin*.tar.gz --directory /tmp/
WORKDIR /tmp/tt/src
RUN ./configure && make && make install

WORKDIR /home/med-scripts