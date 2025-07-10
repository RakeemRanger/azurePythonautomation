import json
import requests
import os
import time

from azure.identity import DefaultAzureCredential

from autocli.lib.CONSTANTS import DEV_AZURE_SUBSCRIPTION
from ..lib.log_util import logClient
from ..lib.azure_clients import AzureClients

class ResourceGroupCreator:
    """
    Class to handle Resource Group creation using Azure REST API.
    """
    def __init__(self, rg_name: str, location: str, trackingId: str):
        self.rg_name = rg_name
        self.location = location
        self.trackingId = str(trackingId)
        self.logger = logClient('azureRGcreate')
        self.subscription_id = DEV_AZURE_SUBSCRIPTION

    def rg_create(self) -> dict:
        logger = self.logger
        trackingId = self.trackingId
        rg_name = self.rg_name
        location = self.location
        api_client = AzureClients().az_group_api_client(
            group_name=rg_name,
            requestType='CREATE',
            body={"location": location}
        )
        try:
            resp = api_client
            correlation_id = resp.headers.get("x-ms-correlation-request-id", "")
            if resp.status_code in (200, 201):
                # Poll for provisioningState Succeeded
                poll_attempts = 30
                poll_interval = 2  # seconds
                rg_status = None
                for _ in range(poll_attempts):
                    status_resp = AzureClients().az_group_api_client(
                        group_name=rg_name,
                        requestType='check'
                    )
                    if status_resp.status_code == 200:
                        rg_status = status_resp.json()
                        state = rg_status.get("properties", {}).get("provisioningState")
                        if state == "Succeeded":
                            break
                        elif state in ("Failed", "Canceled"):
                            logger.error(f"Provisioning failed: {state}")
                            break
                    time.sleep(poll_interval)
                else:
                    state = rg_status.get("properties", {}).get("provisioningState") if rg_status else "Unknown"

                logger.info(f"ResourceGroup: {rg_name} was created with provisioningState: {state} | correlationId: {correlation_id} | trackingId : {trackingId}")
                response = {
                    "name": rg_status.get("name") if rg_status else rg_name,
                    "isProvisioned": "Yes" if state == "Succeeded" else "No",
                    "location": rg_status.get("location") if rg_status else location,
                    "id": rg_status.get("id") if rg_status else "",
                    "ReturnCode": resp.status_code,
                    "message": f"ResourceGroup: {rg_name} was created with provisioningState: {state}",
                    "trackingId": trackingId,
                    "correlationid": correlation_id
                }
                response = json.dumps(response, indent=4)
                logger.info(response)
                return response
            else:
                logger.error(f"Issue creating Resource Group: {rg_name}: {resp.text}")
                response = {
                    "name": rg_name,
                    "isProvisioned": "Unknown",
                    "location": location,
                    "id": "",
                    "ReturnCode": resp.status_code,
                    "message": f"Issue creating Resource Group: {rg_name}: {resp.text}",
                    "trackingId": trackingId,
                    "correlationid": correlation_id
                }
                response = json.dumps(response, indent=4)
                logger.info(response)
                return response
        except Exception as e:
            logger.error(f"Exception creating Resource Group: {rg_name}:\n{e}")
            response = {
                "name": rg_name,
                "isProvisioned": "Unknown",
                "location": location,
                "id": "",
                "ReturnCode": 500,
                "message": f"Exception creating Resource Group: {rg_name}: {e}",
                "trackingId": trackingId,
                "correlationid": ""
            }
            response = json.dumps(response, indent=4)
            logger.info(response)
            return response