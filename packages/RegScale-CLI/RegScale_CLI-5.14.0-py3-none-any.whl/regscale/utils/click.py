"""Provide utilities for interacting with click Objects."""
from typing import Union, Optional, Any, Dict

import click


def process_click_group(
    group: Union[click.Group, click.Command],
    prefix: Optional[str] = None,
) -> Dict[str, Any]:
    """Process a click group into a dictionary
    :param group: a click.Group or click.Command to extract info from
    :param prefix: an optional prefix to name the application, defaults to `group.name`
    """
    prefix = f"{group.name}" if prefix is None else f"{prefix}__{group.name}"
    cmd_dict = {
        "group": group,
        "group_name": prefix,
    }
    for cmd_name, cmd in group.commands.items():
        new_prefix = f"{prefix}__{cmd_name}"
        if isinstance(cmd, click.Group):
            cmd_dict[cmd_name] = process_click_group(cmd, new_prefix)
        elif isinstance(cmd, click.Command):
            cmd_dict[cmd_name] = process_command(cmd, new_prefix)
    return cmd_dict


def process_command(
    cmd: click.Command,
    cmd_name: str,
) -> Dict[str, Any]:
    """Process a click command into a dictionary
    :param cmd: a click.Command object
    :param cmd_name: the name of the command
    """
    return {
        "cmd": cmd,
        "name": cmd_name,
        "params": {
            param.name: process_option(param)
            for param in cmd.params
            if isinstance(param, click.Option)
        },
        "callback": cmd.callback,
    }


def process_option(
    option: click.Option,
) -> Dict[str, Any]:
    """Process a click Option
    :param option: a click Option object
    """
    return {
        "option": option,
        "name": option.name,
        "default": option.default,
        "type": str(option.type),
        "prompt": option.prompt,
        "confirmation_prompt": option.confirmation_prompt,
        "is_flag": option.is_flag,
        "is_bool_flag": option.is_bool_flag,
        "count": option.count,
        "allow_from_autoenv": option.allow_from_autoenv,
        "expose_value": option.expose_value,
        "is_eager": option.is_eager,
        "callback": option.callback,
    }
