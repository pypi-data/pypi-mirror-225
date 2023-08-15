import re
import os
import yaml

import click

from .main import *
from .config import *

@main.group(context_settings=CONTEXT_SETTINGS)
@click.pass_obj
def workspace(env):
    """subcommands for manae workspaces for incstorage"""
    # banner("User", env.__dict__)
    pass


@workspace.command()
@click.option('--foo', default=None)
@click.option('--bar', default=30)
@click.pass_obj
def new(env, foo, bar):
    """Create a new workspace for incstorage"""
    # force config loading
    config.callback()

    # TODO: add your new workspace configuratoin folder here ...



@workspace.command()
@click.pass_obj
def list(env):
    """List existing workspaces for incstorage"""
    # force config loading
    config.callback()

    # TODO: add your new workspace configuratoin folder here ...


