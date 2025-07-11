import click
from autocli.core.az_rg_checker import ResourceGroupChecker
from autocli.core.az_rg_create import ResourceGroupCreator
from autocli.core.az_vnet_checker import VnetChecker
from autocli.core.az_vnet_create import VirtualNetworkCreator
from autocli.core.lib.trackingId_util import TrackingIdGenerator

@click.group()
def cli():
    pass

@cli.command()
@click.argument('rg_name')
@click.argument('location')
def check_rg(rg_name, location):
    """Check if a resource group exists."""
    trackId = TrackingIdGenerator().trackingId()
    checker = ResourceGroupChecker(location=location, rg_name=rg_name, trackingId=trackId)
    print(checker.rg_check())

@cli.command()
@click.argument('rg_name')
@click.argument('location')
def create_rg(rg_name, location):
    """Create a resource group."""
    trackId = TrackingIdGenerator().trackingId()
    creator = ResourceGroupCreator(location=location, rg_name=rg_name, trackingId=trackId)
    print(creator.rg_create())

@cli.command()
@click.argument('rg_name')
@click.argument('location')
@click.argument('vnet_name')
def check_vnet(rg_name, location, vnet_name):
    """Check if a virtual network exists."""
    trackId = TrackingIdGenerator().trackingId()
    checker = VnetChecker(location=location, rg_name=rg_name, vnet_name=vnet_name, trackingId=trackId)
    print(checker.vnet_check())

@cli.command()
@click.argument('rg_name')
@click.argument('location')
@click.argument('vnet_name')
def create_vnet(rg_name, location, vnet_name):
    """Create a virtual network."""
    trackId = TrackingIdGenerator().trackingId()
    creator = VirtualNetworkCreator(rg_name=rg_name, location=location, vnet_name=vnet_name, trackingId=trackId)
    print(creator.vnet_create())

if __name__ == '__main__':
    cli()