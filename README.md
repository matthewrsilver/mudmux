# medmux
A containerized environment with scripts for playing the text-based RPG [Medievia](http://www.medievia.com/), leveraging [tintin++](https://sourceforge.net/projects/tintin/) and tmux.

## Installation and Requirements

The medmux environment runs inside an ubuntu docker container and is indended to be portable, running in both Mac OS and various linux distributions (but see below). While the dependencies for running the game are managed inside the docker container, there are a number of dependencies on the system in which medmux is installed:

* [docker](https://www.docker.com/) is relied upon heavily to run tintin++ and connect to Medievia
* [tmux](https://en.wikipedia.org/wiki/Tmux) is necessary to leverage the full medmux environment
* the [medievia font](http://www.medievia.com/fonts.html) greatly enhances gameplay
* [iTerm2](https://iterm2.com) which makes everything wonderful
* [emacs](https://www.gnu.org/software/emacs/) is currently required though the editor should be made configurable in the future

Note that, at present, useage of certain features of [iTerm2](https://iterm2.com) -- notably its [awesome tmux integration](https://iterm2.com/documentation-tmux-integration.html) and profile switching through [escape codes](https://iterm2.com/documentation-escape-codes.html) -- is hard-coded into medmux, violating the notions of portability described above. A future revision will allow for the configurable usage of these features.

## Building the Docker Container

In the top level directory of medmux, build the `medmux-container` docker container through `docker-compose.yaml` as follows:

```
$ docker-compose build
```

## Running medmux

Once the docker container has been built, medmux can be run any time simply by executing the `mexmux` bash script:

```
$ ./medmux
```

This script creates a tmux session on the host machine with several panels: one for running tintin++ inside a `medmux-container` image, one that tails a log of in-game communications, and one running emacs to allow for editing of text files and note keeping. Each of these panels will automatically run the appropriate content. As discussed above, iTerm2 tmux integration is used, so each of the tmux panels is represented as a native iTerm2 panel, allowing for easy scrolling among many other features.
