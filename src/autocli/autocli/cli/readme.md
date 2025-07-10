# CLI for AzureAutomatioin

This CLI provides command-line access to the core Azure automation logic for resource group and virtual network management.

---

## Overview

The CLI allows you to:
- Check if an Azure Resource Group exists
- Create an Azure Resource Group
- Check if an Azure Virtual Network (VNet) exists
- Create an Azure Virtual Network (VNet)

Each operation generates a unique tracking ID for traceability and logs all actions.

---

## Usage

Navigate to the directory containing `cli.py` or use the module path from your project root.

### **Direct Execution**
```sh
python cli.py <command> [ARGS...]
```

### **Module Execution (from project root)**
```sh
python -m autocli.cli.cli <command> [ARGS...]
```

---

## Commands

### Check Resource Group
```sh
python cli.py check-rg <rg_name> <location>
```
Checks if a resource group exists.

### Create Resource Group
```sh
python cli.py create-rg <rg_name> <location>
```
Creates a new resource group.

### Check Virtual Network
```sh
python cli.py check-vnet <rg_name> <location> <vnet_name>
```
Checks if a virtual network exists in the specified resource group.

### Create Virtual Network
```sh
python cli.py create-vnet <rg_name> <location> <vnet_name>
```
Creates a new virtual network in the specified resource group.

---

## Examples

```sh
python cli.py check-rg demo.eastus.rg eastus
python cli.py create-rg demo.eastus.rg eastus
python cli.py check-vnet demo.eastus.rg eastus demo.eastus.vnet
python cli.py create-vnet demo.eastus.rg eastus demo.eastus.vnet
```

---

## Notes

- Each command generates a unique tracking ID for traceability.
- All operations are logged in JSON format.
- Make sure your Azure credentials and subscription ID are set up before running commands.

---

## Requirements

- Python 3.8+
- Azure CLI authenticated (`az login`)
- Required Python dependencies installed

---

## License

MIT License