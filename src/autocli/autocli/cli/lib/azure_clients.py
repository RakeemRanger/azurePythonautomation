import os
import requests

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential



class AzureClients:
    '''
    Azure Management clients
    '''
    def __init__(self):
        self.subscription = os.getenv('AZURE_SUBSCRIPTION_ID')
        self.credentials = DefaultAzureCredential()

    def az_network_client(self, )-> NetworkManagementClient:
        return NetworkManagementClient(credential=self.credentials,
                                       subscription_id=self.subscription
                                       )
    
    def az_group_client(self, ) -> ResourceManagementClient:
        return ResourceManagementClient(credential=self.credentials,
                                        subscription_id=self.subscription
                                        )