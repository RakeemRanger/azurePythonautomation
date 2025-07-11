import json
import requests
import os

from autocli.core.lib.CONSTANTS import DEV_AZURE_SUBSCRIPTION
from ..core.lib.log_util import logClient
from ..core.lib.azure_clients import AzureClients


class ResourceGroupChecker:
    """
    Class that will handle Resource Group Existence using Azure REST API.
    """

    def __init__(
        self,
        location: str,
        rg_name: str,
        trackingId: str,
    ):
        self.location = location
        self.rg_name = rg_name
        self.logger = logClient("azureRGchecker")
        self.trackingId = str(trackingId)
        # You may want to pass subscription_id explicitly, or fetch from env
        self.subscription_id = DEV_AZURE_SUBSCRIPTION

    def rg_check(self) -> dict:
        logger = self.logger
        trackingId = self.trackingId
        rg_name = self.rg_name
        location = self.location
        api_client = AzureClients().az_group_api_client(group_name=rg_name, requestType="CHECK")
        try:
            resp = api_client
            correlation_id = resp.headers.get("x-ms-correlation-request-id", "")
            if resp.status_code == 200:
                results = resp.json()
                logger.info(
                    f"ResourceGroup: {rg_name} was found | Correlationid: {correlation_id} | trackingId: {trackingId}"
                )
                response = {
                    "name": results.get("name"),
                    "isProvisioned": True,
                    "location": results.get("location"),
                    "id": results.get("id"),
                    "ReturnCode": 200,
                    "message": f"ResourceGroup: {rg_name} was found",
                    "trackingId": trackingId,
                    "correlationid": correlation_id,
                }
                response = json.dumps(response, indent=4)
                return response
            elif resp.status_code == 404:
                response = {
                    "name": rg_name,
                    "isProvisioned": False,
                    "location": location,
                    "id": "",
                    "ReturnCode": 404,
                    "message": f"Resource Group: {rg_name} does not exist.",
                    "trackingId": trackingId,
                    "correlationid": correlation_id,
                }
                response = json.dumps(response, indent=4)
                logger.info(response)
                return response
            else:
                logger.error(f"Issue checking for Resource Group: {rg_name}: {resp.text}")
                response = {
                    "name": rg_name,
                    "isProvisioned": "Unknown",
                    "location": location,
                    "id": "",
                    "ReturnCode": resp.status_code,
                    "message": f"Issue checking for Resource Group: {rg_name}: {resp.text}",
                    "trackingId": trackingId,
                    "correlationid": correlation_id,
                }
                response = json.dumps(response, indent=4)
                logger.info(response)
                return response
        except Exception as e:
            logger.error(f"Exception checking for Resource Group: {rg_name}:\n{e}")
            response = {
                "name": rg_name,
                "isProvisioned": "Unknown",
                "location": location,
                "id": "",
                "ReturnCode": 500,
                "message": f"Exception checking for Resource Group: {rg_name}: {e}",
                "trackingId": trackingId,
                "correlationid": "",
            }
            response = json.dumps(response, indent=4)
            logger.info(response)
            return response
