# AzureAutomatioin

## Overview

**AzureAutomatioin** is a Python-based automation toolkit for managing Azure resources, such as resource groups, using the Azure SDK. It includes utilities for logging, resource group checking/creation, and tracking operations with unique IDs.

## Features

- Create and check Azure Resource Groups
- Logging to file for all operations
- Unique tracking IDs for each operation
- Modular and extensible codebase

## Requirements

- Python 3.8+
- Azure CLI (for authentication)
- Azure SDK for Python (`azure-mgmt-resource`, `azure-identity`, etc.)

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

Run the resource group creation/check script as a module from the project root:

```sh
python -m src.autocli.autocli.cli.az_rg_create
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
│               └── lib/
│                   ├── azure_clients.py
│                   ├── log_util.py
│                   └── trackingId_util.py
├── logs/
├── .gitignore
└── README.md
```

## Logging

All logs are written to the `logs/` directory. Log files are named after the module or operation (e.g., `azureRGchecker.log`).

## License

MIT License

---

**Note:**  
Update this README with more details as your project evolves!