import json
import ipaddress

from .az_rg_checker import ResourceGroupChecker
from .az_rg_create import ResourceGroupCreator
from .az_vnet_checker import VnetChecker
from .lib.azure_clients import AzureClients
from .lib.log_util import logClient
from .lib.trackingId_util import TrackingIdGenerator

class VnetCreate:
    ''''
    Class to check if virtual network resources are available.
    '''
    def __init__(self, location: str, rg_name: str, vnet_name: str, trackingId: str) -> None:
        self.net_client = AzureClients().az_network_client()
        self.trackingId = trackingId
        self.location = location
        self.rg_name = rg_name
        self.vnet_name = vnet_name
        self.logger = logClient('azureVNETcreator')
        self.rg_check = ResourceGroupChecker(location=self.location, rg_name=self.rg_name, trackingId=self.trackingId)

    def prefix_builder(self) -> str:
        """
        Finds the next available /16 VNET prefix by checking all existing VNets in the subscription.
        Returns the next available /16 prefix as a string (e.g., '10.21.0.0/16').
        """
        logger = self.logger
        net_client = self.net_client
        logger.info('Fetching next usable VNET prefix')
        try:
            vnet_prefixes = []
            for vnet in net_client.virtual_networks.list_all():
                for addr_space in vnet.address_space.address_prefixes:
                    if addr_space.endswith('/16'):
                        vnet_prefixes.append(addr_space)
            if not vnet_prefixes:
                logger.info('No existing /16 VNET prefixes found, using default 10.0.0.0/16.')
                return '10.0.0.0/16'
            # Sort prefixes numerically
            vnet_prefixes.sort(key=lambda x: int(ipaddress.IPv4Network(x).network_address))
            last_prefix = vnet_prefixes[-1]
            last_network = ipaddress.IPv4Network(last_prefix)
            # Add 65536 IPs (1 /16 block) to the last network
            next_network = ipaddress.IPv4Network((int(last_network.network_address) + 65536, 16))
            logger.info(f'Next available VNET prefix: {next_network.with_prefixlen}')
            return next_network.with_prefixlen
        except Exception as e:
            logger.error(f"Error fetching next VNET prefix: {e}")
            return '10.0.0.0/16'
        
    def vnet_create(self,) -> dict:
        rg_name = self.rg_name
        location = self.location
        logger = self.logger
        vnet_name = self.vnet_name
        net_client = self.net_client
        trackingId = self.trackingId
        logger.info(f'''starting Virtual Network Check Operation for VNET: {vnet_name}\n
                    {{"trackingId": {trackingId}}}''')
        rg_exist = self.rg_check
        vnet_prefix = self.prefix_builder()
        vnet_check = VnetChecker(location=location, rg_name=rg_name, vnet_name=vnet_name, trackingId=trackingId).vnet_check()
        if isinstance(vnet_check, str):
            vnet_check = json.loads(vnet_check)
        vnet_properties = {"addressSpace": {"addressPrefixes":[vnet_prefix]} }
        vnet_params = {"location": location,  "properties": vnet_properties}
        if rg_exist == 'Yes':
            logger.info(f'Resource Group: {rg_name} has been located.')
            logger.info(f'Will now check if VNET: {vnet_name} exist or not')
            if vnet_check["isProvisioned"]:
                print(vnet_check["isProvisioned"])
                logger.info(f"I have located Virtual Network: {vnet_name}")
                logger.info(f'Virtual Network {vnet_name} was found, nothing to do')
                return vnet_check
            else:
                try:
                    results = net_client.virtual_networks.begin_create_or_update(resource_group_name=rg_name,
                                                           virtual_network_name=vnet_name, parameters=vnet_params
                                                           ).result()
                    response = {
                    "name": results.name,
                    "resourceGroup": rg_name,
                    "isProvisioned": "Yes",
                    "provisioningState": results.provisioning_state,
                    "location": results.location,
                    "id": results.id,
                    "ReturnCode": 200,
                    "message": f"Virtual Network: {vnet_name} created succesfully.",
                    "trackingId": trackingId
                    }
                    response = json.dumps(response, indent=4)
                    logger.info(response)
                    return response
                except Exception as e:
                    response = {
                    "name": rg_name,
                    "resourceGroup": rg_name,
                    "isProvisioned": "Unknown",
                    "provisioningState": "Unknown",
                    "location": location,
                    "id": "",
                    "ReturnCode": 500,
                    "message": f"Issue creating Virtual Network: {vnet_name}:\n{e}",
                    "trackingId": trackingId
                    }
                    response = json.dumps(response, indent=4)
                    logger.info(response)
                    return response
        else:
            rg_create = ResourceGroupCreator(f'demo.{location}.rg', location, trackingId=trackingId).rg_create()
            rg_create = json.loads(rg_create)
            if rg_create["isProvisioned"] == 'Yes' and rg_create["name"] == rg_name:
                logger.info(f"Resource Group: {rg_name} created succesfully.")
                logger.info(f"Moving on to creating Virtual Network: {vnet_name}")
                try:
                    results = net_client.virtual_networks.begin_create_or_update(resource_group_name=rg_name,
                                                           virtual_network_name=vnet_name, parameters=vnet_params
                                                           ).result()
                    response = {
                    "name": results.name,
                    "resourceGroup": rg_name,
                    "isProvisioned": "Yes",
                    "provisioningState": results.provisioning_state,
                    "location": results.location,
                    "id": results.id,
                    "ReturnCode": 200,
                    "message": f"Virtual Network: {vnet_name} created succesfully.",
                    "trackingId": trackingId
                    }
                    response = json.dumps(response, indent=4)
                    logger.info(response)
                    return response
                except Exception as e:
                    response = {
                    "name": vnet_name,
                    "resourceGroup": rg_name,
                    "isProvisioned": "Unknown",
                    "provisioningState": "Unknown",
                    "location": location,
                    "id": "",
                    "ReturnCode": 500,
                    "message": f"Issue creating Virtual Network: {vnet_name}:\n{e}",
                    "trackingId": trackingId
                    }
                    response = json.dumps(response, indent=4)
                    logger.info(response)
                    return response

trackid = TrackingIdGenerator().trackingId()
print(trackid)
ss = VnetCreate('eastus2', 'demo.eastus2.rg', vnet_name='demo.eastus2.vnet', trackingId=trackid).vnet_create()
print(ss)
                




