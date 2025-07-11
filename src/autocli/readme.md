# AzureAutomatioin

## Overview

**AzureAutomatioin** is a Python-based automation toolkit for managing Azure resources (Resource Groups, Virtual Networks, etc.) using the Azure SDK and REST API. It includes utilities for logging, resource group and VNet checking/creation, and tracking operations with unique IDs.

---

## Latest Version & Architecture

**Version Highlights:**
- **Separation of Concerns:**  
  The core logic for Azure resource management (creation, checking, etc.) is now located in the `core/` directory. This logic is imported and reused by both the CLI app and the FastAPI REST API app, ensuring consistent behavior and a single source of truth for all automation operations.
- **Multiple Interfaces:**  
  - **CLI App:** Command-line interface for scripting and direct user interaction.
  - **FastAPI REST API:** HTTP interface for integration with other systems or UIs.
  - Both interfaces call the same core logic, so results and behavior are always in sync.
- **Extensible Design:**  
  You can add more interfaces (e.g., web UI, schedulers) in the future by importing the same core logic.

---

## Features

- Create and check Azure Resource Groups
- Create and check Azure Virtual Networks (VNets)
- Automatic calculation of next available VNet address prefix
- Polling for resource provisioning state to ensure completion
- Logging to file for all operations (JSON format)
- **Correlation ID**: Captures the Azure-side correlation ID for every REST API operation, allowing you to trace and troubleshoot requests in Azure Activity Logs.
- **Tracking ID**: Stamps every operation initiated by the automation app with a unique tracking ID for end-to-end traceability across your automation workflows.
- Modular and extensible codebase

---

## Requirements

- Python 3.8+
- Azure CLI (for authentication)
- Azure SDK for Python (`azure-mgmt-resource`, `azure-mgmt-network`, `azure-identity`, etc.)

---

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

---

## Usage

### Resource Group Creation/Check (CLI)

Run from the project root:
```sh
python -m src.autocli.autocli.cli.cli check-rg <resource-group-name> <location>
python -m src.autocli.autocli.cli.cli create-rg <resource-group-name> <location>
```

### Virtual Network Creation/Check (CLI)

Run from the project root:
```sh
python -m src.autocli.autocli.cli.cli check-vnet <resource-group-name> <location> <vnet-name>
python -m src.autocli.autocli.cli.cli create-vnet <resource-group-name> <location> <vnet-name>
```

### REST API (FastAPI)

Run the FastAPI app (example):
```sh
uvicorn autocli.cli.api.main:app --reload
```
You can then call the REST endpoints for resource group and VNet operations, which use the same core logic as the CLI.

---

#### Example Output (VNet Creation)
```json
{
    "name": "<vnet-name>",
    "resourceGroup": "<resource-group-name>",
    "isProvisioned": "Yes",
    "provisioningState": "Succeeded",
    "location": "<location>",
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.Network/virtualNetworks/<vnet-name>",
    "ReturnCode": 200,
    "message": "Virtual Network: <vnet-name> was created with provisioningState: Succeeded",
    "trackingId": "<uuid>",
    "correlationid": "<azure-correlation-id>"
}
```
- **correlationid**: The Azure-assigned correlation ID for the REST API operation. Use this to trace the request in Azure Activity Logs or for support.
- **trackingId**: The automation app's unique tracking ID for this operation, allowing you to correlate logs and actions across your automation system.

---

## Directory Structure

```
AzureAutomatioin/
├── src/
│   └── autocli/
│       ├── core/
│       │   ├── az_rg_create.py
│       │   ├── az_rg_checker.py
│       │   ├── az_vnet_create.py
│       │   ├── az_vnet_checker.py
│       │   └── ...
│       ├── cli/
│       │   ├── cli.py
│       │   └── ...
│       ├── api/
│       │   ├── azVnetapi.py
│       │   ├── azRGapi.py
│       │   ├── main.py
│       │   └── ...
│       └── lib/
│           ├── azure_clients.py
│           ├── log_util.py
│           ├── trackingId_util.py
│           └── ...
├── logs/
├── .gitignore
└── README.md
```

---

## Logging

All logs are written to the `logs/` directory. Log files are named after the module or operation (e.g., `azureRGchecker.log`, `azureVNETcreator.log`).  
Logs are output in **JSON format** for easy parsing and integration with log management systems.

---

## Notes

- **Single Source of Truth:** All business logic is in `core/`, so CLI and API always behave the same.
- **Extensible:** Add more interfaces or automation entry points as needed by importing from `core/`.
- **Traceability:** Every operation is stamped with both a tracking ID (for your automation) and a correlation ID (from Azure) for full traceability.
- **Security:** The API authentication included is for development only. For production, implement OAuth2 with JWT or another robust authentication method.

---

## License

MIT License

---