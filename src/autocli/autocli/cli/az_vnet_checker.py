import json
import time

from .az_rg_checker import ResourceGroupChecker
from .lib.azure_clients import AzureClients
from .lib.log_util import logClient

class VnetChecker:
    """
    Class to check if virtual network resources are available using Azure REST API.
    """
    def __init__(self, location: str, rg_name: str, vnet_name: str, trackingId: str) -> None:
        self.trackingId = str(trackingId)
        self.location = location
        self.rg_name = rg_name
        self.vnet_name = vnet_name
        self.logger = logClient('azureVNETchecker')
        self.rg_check = ResourceGroupChecker(location=self.location,
                                             rg_name=self.rg_name, trackingId=self.trackingId)

    def vnet_check(self) -> str:
        rg_name = self.rg_name
        location = self.location
        logger = self.logger
        vnet_name = self.vnet_name
        trackingId = self.trackingId

        logger.info(f'''starting Virtual Network Check Operation for VNET: {vnet_name}\n{{"trackingId": {trackingId}}}''')
        # Check if RG exists
        rg_exist = self.rg_check
        if rg_exist:
            logger.info(f'Resource Group: {rg_name} has been located.')
            logger.info(f'Will now check if VNET: {vnet_name} exists or not')
            try:
                # Use REST API to check VNET
                resp = AzureClients().az_vnet_api_client(
                    group_name=rg_name,
                    vnet_name=vnet_name,
                    requestType='check'
                )
                correlation_id = resp.headers.get("x-ms-correlation-request-id", "")
                if resp.status_code == 200:
                    results = resp.json()
                    # Poll for provisioningState Succeeded
                    poll_attempts = 15
                    poll_interval = 2  # seconds
                    vnet_status = results
                    state = vnet_status.get("properties", {}).get("provisioningState")
                    address_prefixes = vnet_status.get("properties", {}).get("addressSpace", {}).get("addressPrefixes", [])
                    vnet_prefix = address_prefixes[0] if address_prefixes else ""
                    for _ in range(poll_attempts):
                        if state == "Succeeded":
                            break
                        elif state in ("Failed", "Canceled"):
                            logger.error(f"Provisioning failed: {state}")
                            break
                        time.sleep(poll_interval)
                        status_resp = AzureClients().az_vnet_api_client(
                            group_name=rg_name,
                            vnet_name=vnet_name,
                            requestType='check'
                        )
                        if status_resp.status_code == 200:
                            vnet_status = status_resp.json()
                            state = vnet_status.get("properties", {}).get("provisioningState")
                            address_prefixes = vnet_status.get("properties", {}).get("addressSpace", {}).get("addressPrefixes", [])
                            vnet_prefix = address_prefixes[0] if address_prefixes else ""
                        else:
                            break

                    response = {
                        "name": vnet_status.get("name") if vnet_status else vnet_name,
                        "addressPrefix": vnet_prefix,
                        "resourceGroup": rg_name,
                        "isProvisioned": "Yes" if state == "Succeeded" else "No",
                        "provisioningState": state,
                        "location": vnet_status.get("location") if vnet_status else location,
                        "id": vnet_status.get("id") if vnet_status else "",
                        "ReturnCode": resp.status_code,
                        "message": f"Virtual Network: {vnet_name} was created with provisioningState: {state}",
                        "trackingId": trackingId,
                        "correlationid": correlation_id
                    }
                    response = json.dumps(response, indent=4)
                    logger.info(response)
                    return response
                elif resp.status_code == 404:
                    response = {
                        "name": vnet_name,
                        "addressPrefix": "",
                        "resourceGroup": rg_name,
                        "isProvisioned": "No",
                        "provisioningState": "NotFound",
                        "location": location,
                        "id": "",
                        "ReturnCode": 404,
                        "message": f"Virtual Network: {vnet_name} Not found.",
                        "trackingId": trackingId,
                        "correlationid": correlation_id
                    }
                    response = json.dumps(response, indent=4)
                    logger.info(response)
                    return response
                else:
                    response = {
                        "name": vnet_name,
                        "addressPrefix": "",
                        "resourceGroup": rg_name,
                        "isProvisioned": "Unknown",
                        "provisioningState": "Unknown",
                        "location": location,
                        "id": "",
                        "ReturnCode": resp.status_code,
                        "message": f"Issue checking for Virtual Network: {vnet_name}: {resp.text}",
                        "trackingId": trackingId,
                        "correlationid": correlation_id
                    }
                    response = json.dumps(response, indent=4)
                    logger.info(response)
                    return response
            except Exception as e:
                logger.error(f"Issue checking for Virtual Network: {vnet_name}:\n{e}")
                response = {
                    "name": vnet_name,
                    "addressPrefix": "",
                    "resourceGroup": rg_name,
                    "isProvisioned": "Unknown",
                    "provisioningState": "Unknown",
                    "location": location,
                    "id": "",
                    "ReturnCode": 500,
                    "message": f"Issue checking for Virtual Network: {vnet_name}:\n{e}",
                    "trackingId": trackingId,
                    "correlationid": ""
                }
                response = json.dumps(response, indent=4)
                logger.info(response)
                return response
        else:
            logger.error(f"Resource Group: {rg_name} not found.")
            response = {
                "name": vnet_name,
                "addressPrefix": "",
                "resourceGroup": rg_name,
                "isProvisioned": "Unknown",
                "provisioningState": "Unknown",
                "location": location,
                "id": "",
                "ReturnCode": 404,
                "message": f"Resource Group: {rg_name} not found.",
                "trackingId": trackingId,
                "correlationid": ""
            }
            response = json.dumps(response, indent=4)
            logger.info(response)
            return response