# API Folder

This folder contains the FastAPI-based REST API endpoints for the AzureAutomatioin project.

---

## Purpose

- The API code in this folder is intended **for development and testing purposes only**.
- It provides a convenient way to interact with the core automation logic via HTTP endpoints during local development.
- The API layer is a thin interface that delegates all Azure operations to the reusable business logic in the `core/` module, ensuring consistency across CLI, API, CI/CD, and other integrations.
- This design allows easy integration with CI/CD pipelines (e.g., Jenkins, GitHub Actions, Azure DevOps) or other automation tools that can make HTTP requests.

---

## Security Notice

- **Current authentication is for development only!**
    - The included authentication (such as HTTP Basic Auth or a dummy bearer token) is not secure for production use.
    - These methods are meant to help developers quickly test and interact with the API.

- **Production Recommendation:**
    - For any production or public deployment, you must implement proper authentication and authorization.
    - **OAuth2 with JWT Bearer tokens** is the recommended approach for securing FastAPI APIs in production.
    - This ensures robust, standards-based security for your endpoints.
    - Also consider adding rate limiting, logging, monitoring, and error handling.

---

## Structure

```
(rranger) nodebrite@nodebrite-ThinkPad-E14-Gen-5:~/Desktop/AzureAutomatioin/src/autocli/autocli/api$ tree -a
.
├── __init__.py
├── main.py
├── models
│   ├── network
│   │   ├── __init__.py
│   │   └── vnet
│   │       └── __init__.py
│   └── rg
│       └── __init__.py
├── __pycache__
│   ├── azRGapi.cpython-312.pyc
│   ├── azVnetapi.cpython-312.pyc
│   ├── __init__.cpython-312.pyc
│   └── main.cpython-312.pyc
├── readme.md
├── routerGenerator.py
├── routers
│   ├── network
│   │   └── vnet
│   │       └── azVnetapi.py
│   └── rg
│       └── azRGapi.py
└── utils
    ├── auth.py
    ├── errors.py
    └── __init__.py
```

- Routers are organized by resource type in `network/vnet/azVnetapi.py` and `rg/azRGapi.py`.
- Models are grouped in `models/network/vnet/` and `models/rg/`.
- Shared utilities are in the `utils/` folder.
- `main.py` imports and includes all routers for the FastAPI app.

---

## Example Usage

- Start the API for development:
    ```sh
    uvicorn autocli.autocli.api.main:app --reload
    ```
- Access the interactive docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Do Not Use in Production As-Is

- The current API is not hardened for security, rate limiting, or error handling.
- Always implement proper authentication (OAuth2/JWT), logging, and monitoring before deploying to production.
- For production, logs should be configured for ingestion into log analytics platforms, and all endpoints should be protected with robust authentication and authorization.

---

## Best Practices

- Keep API modules focused on routing and HTTP interface logic.
- Delegate all Azure operations to the core business logic for consistency.
- Use FastAPI's dependency injection for authentication and validation.
- Document endpoints using FastAPI's built-in OpenAPI docs.

---

## License

MIT License

---