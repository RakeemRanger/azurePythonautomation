import click

@click.group()
def cli():
    pass

from .commands import vnet, rg
from .az_vnet_create import create
