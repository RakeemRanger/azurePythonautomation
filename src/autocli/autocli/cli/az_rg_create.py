import json


from src.autocli.autocli.cli.az_rg_checker import ResourceGroupChecker
from src.autocli.autocli.cli.lib.azure_clients import AzureClients
from src.autocli.autocli.cli.lib.log_util import logClient

class ResourceGroupCreator:
    """
    Class to Manage the creation of Resource Groups
    """
    def __init__(self, rg_name: str, ):
        self.rg_name = rg_name
        self.location = 'canadacentral'
        self.rg_client = AzureClients().az_group_client()
        self.logger = logClient('azureRGcreate')
        self.checker = json.loads(ResourceGroupChecker(self.location, self.rg_name).rg_check())

    def rg_create(self,) -> dict:
        trackingId = self.checker['trackingId']
        rg_exist = self.checker["isProvisioned"]
        rg_name = self.rg_name
        logger = self.logger
        rg_client = self.rg_client
        location = self.location
        if rg_exist:
            response = {
                "name": self.checker["name"],
                "isProvisioned": True,
                "location": self.checker["location"],
                "id": self.checker["id"],
                "ReturnCode": 200,
                "message": f"ResourceGroup: {rg_name} was found",
                "trackingId": trackingId
                }
            response = json.dumps(response, indent=4)
            logger.info(response)
            return response
        else:
            logger.info(f"Starting Resource Group Creation for resource group: {rg_name}")
            try:
                results = rg_client.resource_groups.create_or_update(resource_group_name=rg_name,
                                                                     parameters={"location": location})
                logger.info(f"Resource Group: {rg_name} created successfully")
                response = {
                    "name": results.name,
                    "isProvisioned": True,
                    "location": results.location,
                    "id": results.id,
                    "ReturnCode": 200,
                    "message": f"ResourceGroup: {rg_name} was created successfully",
                    "trackingId": trackingId
                    }
                response = json.dumps(response, indent=4)
                logger.info(response)
                return response
            except Exception as e:
                response = {
                    "name": self.rg_name,
                    "isProvisioned": False,
                    "location": self.location,
                    "id": "",
                    "ReturnCode": 500,
                    "message": f"Issue creating Resource Group: {self.rg_name}:\n{e}",
                    "trackingId": trackingId
                }
                response = json.dumps(response, indent=4)
                logger.info(response)
                return response

        
