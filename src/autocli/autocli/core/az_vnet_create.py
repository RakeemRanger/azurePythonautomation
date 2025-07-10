import json
import ipaddress
import time

from .az_rg_checker import ResourceGroupChecker
from autocli.core.az_rg_create import ResourceGroupCreator
from autocli.lib.CONSTANTS import DEV_AZURE_SUBSCRIPTION
from ..lib.log_util import logClient
from ..lib.azure_clients import AzureClients

class VirtualNetworkCreator:
    """
    Class to handle Virtual Network creation using Azure REST API.
    """
    def __init__(self, rg_name: str, location: str, vnet_name: str, trackingId: str):
        self.rg_name = rg_name
        self.location = location
        self.vnet_name = vnet_name
        self.trackingId = str(trackingId)
        self.logger = logClient('azureVNETcreate')
        self.subscription_id = DEV_AZURE_SUBSCRIPTION

    def prefix_builder(self) -> str:
        """
        Finds the next available /16 VNET prefix by checking all existing VNets in the subscription.
        Returns the next available /16 prefix as a string (e.g., '10.21.0.0/16').
        """
        logger = self.logger
        net_client = AzureClients().az_network_client()
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
            vnet_prefixes.sort(key=lambda x: int(ipaddress.IPv4Network(x).network_address))
            last_prefix = vnet_prefixes[-1]
            last_network = ipaddress.IPv4Network(last_prefix)
            next_network = ipaddress.IPv4Network((int(last_network.network_address) + 65536, 16))
            logger.info(f'Next available VNET prefix: {next_network.with_prefixlen}')
            return next_network.with_prefixlen
        except Exception as e:
            logger.error(f"Error fetching next VNET prefix: {e}")
            return '10.0.0.0/16'

    def vnet_create(self) -> dict:
        logger = self.logger
        trackingId = self.trackingId
        rg_name = self.rg_name
        location = self.location
        vnet_name = self.vnet_name

        # --- Ensure Resource Group exists ---
        rg_check_resp = AzureClients().az_group_api_client(
            group_name=rg_name,
            requestType='check'
        )
        if rg_check_resp.status_code != 200:
            logger.info(f"Resource group {rg_name} not found. Creating it... | correlationId: {correlation_id} | trackingId {trackingId}")
            rg_creator = ResourceGroupCreator(rg_name=rg_name, location=location, trackingId=trackingId)
            rg_create_result = rg_creator.rg_create()
            # Optionally, check if creation succeeded before proceeding
            try:
                rg_create_result_dict = json.loads(rg_create_result)
                if rg_create_result_dict.get("isProvisioned") != "Yes":
                    logger.error(f"Failed to create resource group {rg_name}. Aborting VNet creation.  | correlationId: {correlation_id} | trackingId {trackingId}")
                    return rg_create_result_dict
            except Exception as e:
                logger.error(f"Error parsing RG creation result: {e} | correlationId: {correlation_id} | trackingId {trackingId}")
                return {
                    "name": vnet_name,
                    'addressPrefix': "Unknown",
                    "resourceGroup": rg_name,
                    "isProvisioned": "Unknown",
                    "provisioningState": "Unknown",
                    "location": location,
                    "id": "",
                    "ReturnCode": 500,
                    "message": f"Exception creating Resource Group: {rg_name}: {e}",
                    "trackingId": trackingId,
                    "correlationid": ""
                }

        # Check if VNet exists first
        check_resp = AzureClients().az_vnet_api_client(
            group_name=rg_name,
            vnet_name=vnet_name,
            requestType='check'
        )
        if check_resp.status_code == 200:
            # VNet exists, use its current prefix
            vnet_status = check_resp.json()
            address_prefixes = vnet_status.get("properties", {}).get("addressSpace", {}).get("addressPrefixes", [])
            vnet_prefix = address_prefixes[0] if address_prefixes else self.prefix_builder()
        else:
            # VNet does not exist, use next available prefix
            vnet_prefix = self.prefix_builder()

        vnet_body = {
            "location": location,
            "properties": {
                "addressSpace": {
                    "addressPrefixes": [vnet_prefix]
                }
            }
        }

        api_client = AzureClients().az_vnet_api_client(
            group_name=rg_name,
            vnet_name=vnet_name,
            requestType='CREATE',
            body=vnet_body
        )
        try:
            resp = api_client
            correlation_id = resp.headers.get("x-ms-correlation-request-id", "")
            if resp.status_code in (200, 201):
                # Poll for provisioningState Succeeded
                poll_attempts = 30
                poll_interval = 2  # seconds
                vnet_status = None
                for _ in range(poll_attempts):
                    status_resp = AzureClients().az_vnet_api_client(
                        group_name=rg_name,
                        vnet_name=vnet_name,
                        requestType='check'
                    )
                    if status_resp.status_code == 200:
                        vnet_status = status_resp.json()
                        state = vnet_status.get("properties", {}).get("provisioningState")
                        address_prefixes = vnet_status.get("properties", {}).get("addressSpace", {}).get("addressPrefixes", [])
                        vnet_prefix = address_prefixes[0] if address_prefixes else vnet_prefix
                        if state == "Succeeded":
                            break
                        elif state in ("Failed", "Canceled"):
                            logger.error(f"Provisioning failed: {state}")
                            break
                    time.sleep(poll_interval)
                else:
                    state = vnet_status.get("properties", {}).get("provisioningState") if vnet_status else "Unknown"

                logger.info(f"Virtual Network: {vnet_name} was created with provisioningState: {state}  | correlationId: {correlation_id} | trackingId {trackingId}")
                response = {
                    "name": vnet_status.get("name") if vnet_status else vnet_name,
                    'addressPrefix': vnet_prefix,
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
            else:
                logger.error(f"Issue creating Virtual Network: {vnet_name}: {resp.text} | correlationId: {correlation_id} | trackingId {trackingId}")
                response = {
                    "name": vnet_name,
                    'addressPrefix': "Unknown",
                    "resourceGroup": rg_name,
                    "isProvisioned": "Unknown",
                    "provisioningState": "Unknown",
                    "location": location,
                    "id": "",
                    "ReturnCode": resp.status_code,
                    "message": f"Issue creating Virtual Network: {vnet_name}: {resp.text}",
                    "trackingId": trackingId,
                    "correlationid": correlation_id
                }
                response = json.dumps(response, indent=4)
                logger.info(response)
                return response
        except Exception as e:
            logger.error(f"Exception creating Virtual Network: {vnet_name}:\n{e}\n| correlationId: {correlation_id} | trackingId {trackingId}")
            response = {
                "name": vnet_name,
                'addressPrefix': "Unknown",
                "resourceGroup": rg_name,
                "isProvisioned": "Unknown",
                "provisioningState": "Unknown",
                "location": location,
                "id": "",
                "ReturnCode": 500,
                "message": f"Exception creating Virtual Network: {vnet_name}: {e}",
                "trackingId": trackingId,
                "correlationid": ""
            }
            response = json.dumps(response, indent=4)
            logger.info(response)
            return response

