#!/usr/bin/env python

"""
mudmux - a python script for launching the mudmux tmux environment

This file uses the contents of the config.yaml file to set environment
variables, build a tmux session with tmuxp based on the tmux.yaml config file
that leverages those environment variables, and launches the tmux session.
"""

import collections.abc
import os
import pathlib
import yaml

from typing import Optional


MUDMUX_BASE_PATH = os.path.dirname(__file__)
os.environ['MUDMUX_BASE_PATH'] = MUDMUX_BASE_PATH
os.environ['COMPOSE_FILE'] = f'{MUDMUX_BASE_PATH}/docker-compose.yaml'

USER_HOME_DIR = os.environ['HOME']
USER_MUDMUX_DIR = f'{USER_HOME_DIR}/.mudmux.d'
os.environ['MUDMUX_USER_DIR'] = USER_MUDMUX_DIR

CONFIG_FILE_PATH = f'{MUDMUX_BASE_PATH}/config/config.yaml'
TMUX_CONFIG_PATH = f'{MUDMUX_BASE_PATH}/config/tmux.yaml'


def _update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = _update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


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


def _load_config_yaml(cfg_path: str) -> dict:
    """
    Load a yaml config file for mudmux.

    Args:
      - cfg_path: a string containing a path to the config yaml file

    Returns:
      A dictionary representation of the config
    """
    with open(cfg_path) as cfg_file:
        return yaml.safe_load(cfg_file)


def load_user_config_override() -> dict:
    """
    Load the user's config override from `USER_MUDMUX_DIR` if it exists.

    Returns:
      A dictionary representation of the user's config override
    """
    user_dir_exists = os.path.isdir(USER_MUDMUX_DIR)
    user_config_file = f'{USER_MUDMUX_DIR}/config.yaml'
    user_config_exists = os.path.isfile(user_config_file)
    if user_dir_exists and user_config_exists:
        return _load_config_yaml(user_config_file)
    return {}


def load_config() -> dict:
    """
    Load the configuration for mudmux, allowing a user's configuration
    to override the default.

    Returns:
      A dictionary representation of the config
    """
    default_config = _load_config_yaml(CONFIG_FILE_PATH)
    user_config = load_user_config_override()
    return _update(default_config, user_config)


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

    comms_log_path = os.path.expandvars(cfg['log_dir'])
    comms_log_name = cfg['log_file_name']
    os.environ['MUDMUX_COMMS_LOG'] = f'{comms_log_path}/{comms_log_name}'

    notes_file_dir = os.path.expandvars(cfg['notes_file_dir'])
    notes_file_name = cfg['notes_file_name']
    os.environ['MUDMUX_NOTES_FILE'] = f'{notes_file_dir}/{notes_file_name}'

    chat_cfg_dir = os.path.expandvars(cfg['chat_config_dir'])
    chat_cfg_name = cfg['chat_config_file_name']
    os.environ['MUDMUX_CHAT_CONFIG_FILE'] = f'{chat_cfg_dir}/{chat_cfg_name}'


def main() -> None:
    """Main mudmux runner"""

    # Load configuration and prepare the environment
    config = load_config()
    set_environment_from_config(config)
    pathlib.Path(os.environ['MUDMUX_COMMS_LOG']).touch()
    pathlib.Path(os.environ['MUDMUX_NOTES_FILE']).touch()

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
