# mudmux
A containerized environment with scripts for playing the text-based RPG [Medievia](http://www.medievia.com/), leveraging [tintin++](https://sourceforge.net/projects/tintin/) and tmux.

## Installation and Requirements

The mudmux environment leverages an ubuntu docker container and is indended to be portable, running in both Mac OS and various linux distributions (but see below). While the dependencies for running the game are managed inside the docker container, there are a number of dependencies on the system in which mudmux is installed:

* [python](https://www.python.org/) is used to install, launch and manage mudmux; developed on 3.9
* [docker](https://www.docker.com/) is relied upon heavily to run tintin++ and connect to Medievia
* [tmux](https://en.wikipedia.org/wiki/Tmux) is necessary to leverage the full mudmux environment

With those requirements satisfied, the latest version of mudmux can be install via pip directly from github:

```
python -m pip install git+https://github.com/matthewrsilver/mudmux.git
```

### Using iTerm2's tmux integration and profiles

By default, certain features of [iTerm2](https://iterm2.com) -- notably its [awesome tmux integration](https://iterm2.com/documentation-tmux-integration.html) and profile switching through [escape codes](https://iterm2.com/documentation-escape-codes.html) -- are used by mudmux. When iTerm2 isn't available or isn't desired, mudmux can be configured to run tmux without iTerm2 integration and profile switching.

When leveraging iTerm2's features, it's valuable to have a game-specific profile configured for use within mudmux. There are a handful of requirements placed on iTerm2 settings and on this profile that help:

* Tell iTerm2 not to automatically switch to the tmux profile (Preferences -> General -> tmux) as described in [this iTerm2 thread](https://gitlab.com/gnachman/iterm2/-/issues/4543#note_326526076).
* For Medievia, specifically, the [medievia font](http://www.medievia.com/fonts.html) greatly enhances gameplay, and can be set as the default font in the profile

## Running mudmux

Once installed via pip, mudmux can be run from the command line:

```
$ mudmux
```

This script creates a tmux session on the host machine with several panes: one for running tintin++ inside a `mudmux-container` image, one that tails a log of in-game communications, and one running an editor to allow for note keeping. Each of these panes will automatically run the appropriate content. As discussed above, iTerm2 tmux integration is used, so each of the tmux panes is represented as a native iTerm2 pane, allowing for easy scrolling among many other features.

![Medievia in mudmux](data/medievia_in_mudmux.png)

### Running or restarting tintin

Sometimes it may be useful to run tintin by itself outside of mudmux. Alternatively, there are a variety of circumstances (crashes, accidentally sending `#end` rather than `#zap`, and so on)  under which one might need to run tintin again while the tmux session is still attached.

To do so, simply run the tintin service through docker from the nested `mudmux` directory:

```
$ docker-compose run tintin
```

This will create and attach to the docker, run tintin, and exit once tintin finishes.

Note that there are a number of environment variables that are not correctly set under these conditions, so this should be used with care.

## Connecting to Medievia

The full-height left pane starts tintin and loads all scripts but does not connect to Medievia, or any other game for that matter. Bcause mudmux is today heavily integrated with Medievia, commands to connect are already available. To start a session to medievia called `med`, just run the following at the tintin prompt:

```
connect
```

If credentials have been provided in the `config` directory (as described below) then connecting to chat is as simple as:

```
chat_connect
```

From here, interacting with tintin and Medievia occurs as normal; quit the Medievia session with tintin's `#zap` command and close tintin with `#end`.

## Configuring mudmux

All configuration is handled in the `mudmux/config` directory; values that might reasonably be changed are in the `config.yaml` file.

But once mudmux is installed via pip, configuration files are pretty buried. To make configuration easier, mudmux supports user configs which override the default config. To override, create a directory in `$HOME` called `.mudmux.d` and add a `config.yaml` file there. An example user config could look like:

```shell
matt@computer:~$ cat ~/.mudmux.d/config.yaml
editor: "emacs"
iterm:
  mudmux_iterm_profile: "med"
chat_config_dir: "${MUDMUX_USER_DIR}"
log_dir: "${MUDMUX_USER_DIR}"
notes_file_dir: "${MUDMUX_USER_DIR}"
```

Here, the editor can be changed from `emacs` to whatever inferior editor might be preferred. Also, iTerm2 tmux integration can be disabled, and the name of the iTerm2 profile to be used can be set (or left blank to prevent switching. Further, chat configuration, log files, and notes files, can all live in arbitrary locations. Absolute paths are necessary, and the $MUDMUX_USER_DIR environment variable, pointing to `$HOME/.mudmux.d` is available when this config is loaded.