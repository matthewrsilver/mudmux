#!/usr/bin/env python

"""
mudmux - a python script for launching the mudmux tmux environment

This file uses the contents of the config.yaml file to set environment
variables, build a tmux session with tmuxp based on the tmux.yaml config file
that leverages those environment variables, and launches the tmux session.
"""

import os
import pathlib
import yaml

from typing import Optional


MUDMUX_BASE_PATH = os.path.dirname(__file__)
os.environ['MUDMUX_BASE_PATH'] = MUDMUX_BASE_PATH
os.environ['COMPOSE_FILE'] = f'{MUDMUX_BASE_PATH}/docker-compose.yaml'

CONFIG_FILE_PATH = f'{MUDMUX_BASE_PATH}/config/config.yaml'
TMUX_CONFIG_PATH = f'{MUDMUX_BASE_PATH}/config/tmux.yaml'

pathlib.Path(f'{MUDMUX_BASE_PATH}/logs/communications.log').touch()
pathlib.Path(f'{MUDMUX_BASE_PATH}/data/notes.txt').touch()


def construct_profile_escape(profile_name: Optional[str] = None) -> str:
    """
    Set up a profile escape string to trigger iterm profile switching.

    If no name is provided or if it is empty, an empty string is returned.

    Args:
      - profile_name: a string profile name (optional)

    Returns:
      An escape string or an empty string.
    """
    return f'\033]50;SetProfile={profile_name}\a' if profile_name else ''


def load_config(cfg_path: str) -> dict:
    """
    Load the yaml config for mudmux.

    Args:
      - cfg_path: a string containing a path to the config yaml file

    Returns:
      A dictionary representation of the config
    """
    with open(cfg_path) as cfg_file:
        return yaml.safe_load(cfg_file)


def set_environment_from_config(cfg: dict) -> None:
    """
    Set environment variables from a loaded config file.

    Args:
      - cfg: a dictionary with config info, likely parsed from yaml
    """
    os.environ['MUDMUX_TMUX_SESSION_NAME'] = cfg['tmux_session_name']
    os.environ['MUDMUX_EDITOR'] = cfg['editor']

    iterm_profile = cfg['iterm'].get('mudmux_iterm_profile')
    os.environ['MUDMUX_PROFILE_ESC'] = construct_profile_escape(iterm_profile)


def main() -> None:
    """Main mudmux runner"""

    # Set environment variables
    config = load_config(CONFIG_FILE_PATH)
    set_environment_from_config(config)

    # Unpack a few locally useful values
    use_iterm_tmux_integration = config['iterm'].get('enable_tmux_integration')
    tmux_CC_flag = '-CC' if use_iterm_tmux_integration else ''
    tmux_session_name = config['tmux_session_name']

    # Execute tmux commands
    tmuxp_load_cmd = f'tmuxp load -d {TMUX_CONFIG_PATH}'
    tmux_attach_cmd = f'tmux {tmux_CC_flag} attach -t {tmux_session_name}'
    tmux_cmd = f'{tmuxp_load_cmd} && {tmux_attach_cmd}'
    os.system(tmux_cmd)


if __name__ == '__main__':
    main()
