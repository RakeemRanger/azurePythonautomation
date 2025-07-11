# Lib Folder

This folder contains shared utility modules for the AzureAutomatioin project.

---

## Purpose

The `lib/` directory provides reusable helper functions, classes, and constants that support the core business logic, CLI, and API layers.  
These utilities are not specific to any single interface or business domain, but instead offer common functionality needed throughout the project.

---

## Typical Contents

- **Azure SDK/REST API clients**  
  Classes and functions for authenticating and interacting with Azure services.

- **Logging utilities**  
  Helpers for consistent, JSON-formatted logging across all modules.

- **Tracking and ID generation**  
  Utilities for generating unique tracking IDs for traceability.

- **Constants**  
  Centralized configuration values (e.g., log folder paths, subscription IDs).

---

## Example Structure

```
lib/
├── azure_clients.py
├── log_util.py
├── trackingId_util.py
├── CONSTANTS.py
└── (other utility modules)
```

---

## Usage

- Import utilities from `lib/` in your `core/`, `cli/`, or `api/` modules as needed.
- Do **not** put business logic or interface-specific code in this folder.
- Keep this folder focused on generic, reusable helpers.

---

## Best Practices

- Keep utility code modular and interface-agnostic.
- Document each utility for clarity and maintainability.
- Use JSON logging for easy integration with log analytics platforms.

---

## License

MIT License