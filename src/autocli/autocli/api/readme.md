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

---

## Structure

- Each API module (e.g., `azVnetapi.py`, `azRGapi.py`) defines an `APIRouter` with endpoints for a specific resource type.
- All routers are included in a single FastAPI app via `main.py`.
- The API layer does not contain business logic; it simply calls into the `core/` module.

---

## Example Usage

- Start the API for development:
    ```sh
    uvicorn autocli.cli.api.main:app --reload
    ```
- Access the interactive docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Do Not Use in Production As-Is

- The current API is not hardened for security, rate limiting, or error handling.
- Always implement proper authentication (OAuth2/JWT), logging, and monitoring before deploying to production.
- For production, logs should be configured for ingestion into log analytics platforms, and all endpoints should be protected with robust authentication and authorization.

---

## License

MIT License

---