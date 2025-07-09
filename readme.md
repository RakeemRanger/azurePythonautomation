# AzureAutomatioin

## Overview

**AzureAutomatioin** is a Python-based automation toolkit for managing Azure resources (Resource Groups, Virtual Networks, etc.) using the Azure SDK. It includes utilities for logging, resource group and VNet checking/creation, and tracking operations with unique IDs.

## Features

- Create and check Azure Resource Groups
- Create and check Azure Virtual Networks (VNets)
- Automatic calculation of next available VNet address prefix
- Logging to file for all operations
- Unique tracking IDs for each operation
- Modular and extensible codebase

## Requirements

- Python 3.8+
- Azure CLI (for authentication)
- Azure SDK for Python (`azure-mgmt-resource`, `azure-mgmt-network`, `azure-identity`, etc.)

## Setup

1. **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd AzureAutomatioin
    ```

2. **Create and activate a virtual environment (recommended):**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set your Azure Subscription ID:**
    ```sh
    export AZURE_SUBSCRIPTION_ID=<your-subscription-id>
    ```

5. **Login to Azure CLI (if not already):**
    ```sh
    az login
    ```

## Usage

### Resource Group Creation/Check

Run from the project root:
```sh
python -m src.autocli.autocli.cli.az_rg_create
```

### Virtual Network Creation/Check

Run from the project root:
```sh
python -m src.autocli.autocli.cli.az_vnet_create
```

#### Example Output (VNet Creation)
```json
{
    "name": "<vnet-name>",
    "resourceGroup": "<resource-group-name>",
    "isProvisioned": true,
    "provisioningState": "Succeeded",
    "location": "<location>",
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.Network/virtualNetworks/<vnet-name>",
    "ReturnCode": 200,
    "message": "Virtual Network: <vnet-name> has been located.",
    "trackingId": "<uuid>"
}
```

## Directory Structure

```
AzureAutomatioin/
├── src/
│   └── autocli/
│       └── autocli/
│           └── cli/
│               ├── az_rg_create.py
│               ├── az_rg_checker.py
│               ├── az_vnet_create.py
│               ├── az_vnet_checker.py
│               └── lib/
│                   ├── azure_clients.py
│                   ├── log_util.py
│                   ├── trackingId_util.py
│                   └── ...
├── logs/
├── .gitignore
└── README.md
```

## Logging

All logs are written to the `logs/` directory. Log files are named after the module or operation (e.g., `azureRGchecker.log`, `azureVNETcreator.log`).

## License

MIT License

---

**Note:**  
Update this README with more details as your project evolves!