import json

from azure.core.exceptions import ResourceNotFoundError
from src.autocli.autocli.cli.lib.log_util import logClient
from src.autocli.autocli.cli.lib.azure_clients import AzureClients
from src.autocli.autocli.cli.lib.trackingId_util import TrackingIdGenerator

class ResourceGroupChecker:
    """
    Class that will handle Resource Group Existence
    """
    def __init__(self, location: str, rg_name: str):
        self.location = location
        self.rg_name = rg_name
        self.rg_client = AzureClients().az_group_client()
        self.logger = logClient('azureRGchecker')
    
    def rg_check(self, ) -> dict:
        """
        Method to check if a resource group exist or not.
        """
        logger = self.logger
        trackingId = str(TrackingIdGenerator().trackingId())
        rg_client = self.rg_client
        try:
            results = rg_client.resource_groups.get(
            resource_group_name=self.rg_name
            )
            logger.info(f'ResourceGroup: {self.rg_name} was found')
            response = {
                "name": results.name,
                "isProvisioned": True,
                "location": results.location,
                "id": results.id,
                "ReturnCode": 200,
                "message": f"ResourceGroup: {self.rg_name} was found",
                "trackingId": trackingId
                }
            response = json.dumps(response, indent=4)
            return response
        except ResourceNotFoundError as e:
            response = {
                "name": self.rg_name,
                "isProvisioned": False,
                "location": self.location,
                "id": "",
                "ReturnCode": 404,
                "message": f"Resource Group: {self.rg_name} does not exist:\n{e}",
                "trackingId": trackingId
                }
            response = json.dumps(response, indent=4)
            logger.info(response)
            return response
        except Exception as e:
            logger.error(f'Issue checking for Resource Group: {self.rg_name}:\n{e}')
            response = {
                "name": self.rg_name,
                "isProvisioned": "Unknown",
                "location": self.location,
                "id": "",
                "ReturnCode": 500,
                "message": f"Issue checking for Resource Group: {self.rg_name}:",
                "trackingId": trackingId
                }
            response = json.dumps(response, indent=4)
            logger.info(response)
            return response