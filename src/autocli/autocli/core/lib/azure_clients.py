import os
import requests

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient

from autocli.core.lib.CONSTANTS import DEV_AZURE_SUBSCRIPTION


class AzureClients:
    """
    Azure Management clients
    """

    def __init__(self):
        self.subscription = DEV_AZURE_SUBSCRIPTION
        self.credentials = DefaultAzureCredential()

    def az_network_client(self):
        credential = DefaultAzureCredential()
        subscription = self.subscription
        return NetworkManagementClient(credential, subscription_id=subscription)

    def az_group_api_client(self, group_name: str, requestType: str, body: dict = None):
        credential = self.credentials
        subscription_id = self.subscription
        token = credential.get_token("https://management.azure.com/.default")
        api_version = "2022-09-01"
        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{group_name}?api-version={api_version}"
        headers = {"Authorization": f"Bearer {token.token}", "Content-Type": "application/json"}
        if requestType.lower() == "check":
            return requests.get(url=url, headers=headers)
        elif requestType.lower() == "create":
            if not body:
                raise ValueError("Body with at least a 'location' key is required to create a resource group.")
            return requests.put(url=url, headers=headers, json=body)
        elif requestType.lower() == "delete":
            return requests.delete(url=url, headers=headers)
        else:
            return None

    def az_vnet_api_client(self, group_name: str, vnet_name: str, requestType: str, body: dict = None):
        credential = self.credentials
        subscription_id = self.subscription
        token = credential.get_token("https://management.azure.com/.default")
        api_version = "2022-09-01"
        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{group_name}/providers/Microsoft.Network/virtualNetworks/{vnet_name}?api-version={api_version}"
        list_rg_url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{group_name}/providers/Microsoft.Network/virtualNetworks?api-version={api_version}"
        list_all_url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Network/virtualNetworks?api-version={api_version}"
        headers = {"Authorization": f"Bearer {token.token}", "Content-Type": "application/json"}
        if requestType.lower() == "check":
            return requests.get(url=url, headers=headers)
        elif requestType.lower() == "create":
            return requests.put(url=url, headers=headers, json=body)
        elif requestType.lower() == "delete":
            return requests.delete(url=url, headers=headers)
        elif requestType.lower() == "list_rg":
            return requests.get(url=list_rg_url, headers=headers)
        elif requestType.lower() == "list_all":
            return requests.get(url=list_all_url, headers=headers)
        else:
            return None

    def az_subnet_api_client(
        self, group_name: str, vnet_name: str, subnet_name: str, requestType: str, body: dict = None
    ):
        credential = self.credentials
        subscription_id = self.subscription
        token = credential.get_token("https://management.azure.com/.default")
        api_version = "2022-09-01"
        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{group_name}/providers/Microsoft.Network/virtualNetworks/{vnet_name}/subnets/{subnet_name}?api-version={api_version}"
        headers = {"Authorization": f"Bearer {token.token}", "Content-Type": "application/json"}
        if requestType.lower() == "check":
            return requests.get(url=url, headers=headers)
        elif requestType.lower() == "create":
            return requests.put(url=url, headers=headers, json=body)
        elif requestType.lower() == "delete":
            return requests.delete(url=url, headers=headers)
        else:
            return None
