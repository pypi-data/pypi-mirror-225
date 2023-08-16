"""Provide utilities to help using the drip_drip module"""

from typing import Dict, List, Optional, Union

from argparse import Namespace
from configparser import ConfigParser
from pathlib import Path
import os

DEFAULT_INI_FILE = "drip_feed.ini"


Configs = dict[str, Union[bool, int, str, None]]


def find_config(config_file: Optional[str]) -> Path:
    """
    Returns the configuration file depending on the value of the config file passed.

    Args:
        config_file: the name, if any, of the config file to find.

    Returns:
        the path to the found config file

    Raises:
        ValueError: when no config file can be found.
    """
    if None is config_file:
        if "HOME" in os.environ:
            result = os.path.join(os.environ["HOME"], DEFAULT_INI_FILE)
        else:
            raise ValueError(
                "Can not find INI file $HOME/"
                + DEFAULT_INI_FILE
                + ", make sure HOME is defined"
            )
    else:
        result = config_file
    if not os.path.exists(result):
        raise ValueError("Can not find INI file " + result + ", it does not exist")
    return Path(result)


def read_envar_values(mapping: Dict[str, str]) -> Namespace:
    """
    Create a argparse.Namespace instance populated by the values of the
    envrionmental variables specified by the keys of the mapping.

    Args:
        mapping: the mapping of environmental variables to the
                matching option name.
    """
    result = {}
    for key in mapping.keys():
        value = os.getenv(key)
        if None is not value:
            option = mapping[key]
            result[option] = value
    return Namespace(**result)


def read_config(  # pylint: disable=too-many-arguments, too-many-branches
    config_file: str,
    section: str,
    strings: Optional[List[str]] = None,
    integers: Optional[List[str]] = None,
    booleans: Optional[List[str]] = None,
) -> Configs:
    """
    Reads the supplied configuration ini

    Args:
        config_file: the path to the file containing the configuration information.
        section: the section within the file containing the configuration for this instance.
        booleans: a List of keys that should be returned as strings.
        booleans: a List of keys that should be returned as bools.
        integers: a List of keys that should be returned as integers.
    """

    config_parser = ConfigParser()
    filepath = find_config(config_file)

    config_parser.read(filepath)
    config: Configs = {}
    for option in config_parser.options(section):
        try:
            if None is not strings and option in strings:
                config[option] = config_parser.get(section, option)
            if None is not integers and option in integers:
                config[option] = config_parser.getint(section, option)
            elif None is not booleans and option in booleans:
                config[option] = config_parser.getboolean(section, option)
            else:
                config[option] = config_parser.get(section, option)
        except:  # pylint: disable=bare-except
            config[option] = None

    if None is not strings:
        for option in strings:
            if not option in config:
                config[option] = None

    if None is not integers:
        for option in integers:
            if not option in config:
                config[option] = None

    if None is not booleans:
        for option in booleans:
            if not option in config:
                config[option] = None

    return config
