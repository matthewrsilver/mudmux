# mudmux
A containerized environment with scripts for playing the text-based RPG [Medievia](http://www.medievia.com/), leveraging [tintin++](https://sourceforge.net/projects/tintin/) and tmux.

## Installation and Requirements

The mudmux environment runs inside an ubuntu docker container and is indended to be portable, running in both Mac OS and various linux distributions (but see below). While the dependencies for running the game are managed inside the docker container, there are a number of dependencies on the system in which mudmux is installed:

* [docker](https://www.docker.com/) is relied upon heavily to run tintin++ and connect to Medievia
* [tmux](https://en.wikipedia.org/wiki/Tmux) is necessary to leverage the full mudmux environment
* the [medievia font](http://www.medievia.com/fonts.html) greatly enhances gameplay
* [iTerm2](https://iterm2.com) which makes everything wonderful
* [emacs](https://www.gnu.org/software/emacs/) is currently required though the editor should be made configurable in the future
* [tmuxp==1.3.2](https://github.com/tmux-python/tmuxp) is used to read the appropriate panel layout for tmux from a yaml file, but must be pinned to this version to avoid some issues
* [click==7.1.2](https://pypi.org/project/click/) is a dependency of tmuxp, but must be pinned to this version to avoid some issues

Note that, at present, useage of certain features of [iTerm2](https://iterm2.com) -- notably its [awesome tmux integration](https://iterm2.com/documentation-tmux-integration.html) and profile switching through [escape codes](https://iterm2.com/documentation-escape-codes.html) -- is hard-coded into mudmux, violating the notions of portability described above. A future revision will allow for the configurable usage of these features.

## Building the Docker Container

In the top level directory of mudmux, build the `mudmux-container` docker container through `docker-compose.yaml` as follows:

```
$ docker-compose build
```

## Running mudmux

Once the docker container has been built, mudmux can be run any time simply by executing the `mudmux` bash script:

```
$ ./mudmux
```

This script creates a tmux session on the host machine with several panels: one for running tintin++ inside a `mudmux-container` image, one that tails a log of in-game communications, and one running emacs to allow for editing of text files and note keeping. Each of these panels will automatically run the appropriate content. As discussed above, iTerm2 tmux integration is used, so each of the tmux panels is represented as a native iTerm2 panel, allowing for easy scrolling among many other features.

![Medievia in mudmux](data/medievia_in_mudmux.png)

### Running or restarting tintin

Sometimes it may be useful to run tintin by itself outside of mudmux. Alternatively, there are a variety of circumstances (crashes, accidentally sending `#end` rather than `#zap`, and so on)  under which one might need to run tintin again while the tmux session is still attached.

To do so, simply run the tintin service through docker:

```
docker-compose run tintin
```

This will create and attach to the docker, run tintin, and exit once tintin finishes.

## Connecting to Medievia

The full-height left panel starts tintin and loads all scripts but does not connect to Medievia, or any other game for that matter. Bcause mudmux is today heavily integrated with Medievia, commands to connect are already available. To start a session to medievia called `med`, just run the following at the tintin prompt:

```
connect
```

If credentials have been provided in the `config` directory (as described below) then connecting to chat is as simple as:

```
chat_connect
```

From here, interacting with tintin and Medievia occurs as normal; quit the Medievia session with tintin's `#zap` command and close tintin with `#end`.
