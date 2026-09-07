# Phase 5: Claude Desktop Integration & Documentation — Research

## Implementation Approach
Phase 5 finalizes the deployment and developer experience package:

1. **Claude Desktop Configuration (`claude_desktop_config.example.json`)**:
   - Outlines exact JSON syntax for registering `AzureTelemetryBridge` in Claude Desktop's stdio configuration.
   - Platform paths:
     - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
     - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Configures `command`, `args`, and environment variables (`AZURE_STORAGE_ACCOUNT_NAME`, `AZURE_CONTAINER_NAME`, `AZURE_BLOB_NAME`).

2. **Enterprise Production `README.md`**:
   - Executive and technical documentation.
   - System architecture diagram (Mermaid) illustrating stdio protocol communication between Claude Desktop, FastMCP server, DefaultAzureCredential, Azure Blob Storage, and the FinOps calculation engine.
   - Complete step-by-step guides for:
     - Local installation and offline mock mode.
     - Terraform infrastructure provisioning and Entra ID RBAC configuration.
     - Pytest test execution and Ruff linting/formatting.
     - Claude Desktop live connection.

3. **Final Quality Audit**:
   - Full test run (`pytest -v tests/`).
   - Full lint/formatting audit (`ruff check .`, `ruff format --check .`).
   - Terraform formatting and validation (`terraform fmt -check`, `terraform validate`).

---
*Researched: 2026-09-07*
