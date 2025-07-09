import json

from azure.core.exceptions import ResourceNotFoundError

from src.autocli.autocli.cli.az_rg_checker import ResourceGroupChecker
from src.autocli.autocli.cli.lib.azure_clients import AzureClients
from src.autocli.autocli.cli.lib.log_util import logClient
from src.autocli.autocli.cli.lib.trackingId_util import TrackingIdGenerator

class VnetChecker:
    ''''
    Class to check if virtual network resources are available.
    '''
    def __init__(self, location: str, rg_name: str, vnet_name: str) -> None:
        self.net_client = AzureClients().az_network_client()
        self.location = location
        self.rg_name = rg_name
        self.vnet_name = vnet_name
        self.logger = logClient('azureVNETchecker')
        self.rg_check = ResourceGroupChecker(location=self.location,
                                             rg_name=self.rg_name)

    def vnet_check(self,) -> dict:
        rg_name = self.rg_name
        location = self.location
        logger = self.logger
        vnet_name = self.vnet_name
        net_client = self.net_client
        trackingId = str(TrackingIdGenerator().trackingId())
        logger.info(f'''starting Virtual Network Check Operation for VNET: {vnet_name}\n
                    {{"trackingId": {trackingId}}}''')
        rg_exist = self.rg_check
        if rg_exist:
            logger.info(f'Resource Group: {rg_name} has been located.')
            logger.info(f'Will now check if VNET: {vnet_name} exist or not')
            try:
                results = net_client.virtual_networks.get(resource_group_name=rg_name,
                                                           virtual_network_name=vnet_name
                                                           )
                response = {
                "name": results.name,
                "isProvisioned": True,
                "provisioningState": results.provisioning_state,
                "location": results.location,
                "id": results.id,
                "ReturnCode": 200,
                "message": f"Virtual Network: {vnet_name} has been located.",
                "trackingId": trackingId
                }
                response = json.dumps(response, indent=4)
                logger.info(response)
                return response
            except ResourceNotFoundError as e:
                response = {
                "name": rg_name,
                "isProvisioned": "Unknown",
                "provisioningState": "Unknown",
                "location": location,
                "id": "",
                "ReturnCode": 404,
                "message": f"Virtual Network: {vnet_name} Not found:\n{e}",
                "trackingId": trackingId
                }
                response = json.dumps(response, indent=4)
                logger.info(response)
                return response
            except Exception as e:
                response = {
                "name": rg_name,
                "isProvisioned": "Unknown",
                "provisioningState": "Unknown",
                "location": location,
                "id": "",
                "ReturnCode": 500,
                "message": f"Issue checking for Virtual Network: {vnet_name}:\n{e}",
                "trackingId": trackingId
                }
                logger.info(response)
                return response

ss = VnetChecker('canadacentral','ad.rg', 'dc01-vnet').vnet_check()
print(ss)