# Pitfalls Research: Claude Desktop MCP & Azure Integrations

**Domain:** MCP Server Development, Claude Desktop Stdio Transport, Azure Blob SDK  
**Date:** 2026-09-07  
**Status:** Complete  

## Critical Pitfalls & Mitigations

### 1. `stdout` Pollution Breaking JSON-RPC Protocol
- **Pitfall**: In MCP servers operating over stdio, any output to `stdout` (e.g. `print()`, informational library messages, unhandled warnings) corrupts the JSON-RPC stream, causing Claude Desktop to crash or report `Server disconnected`.
- **Mitigation**: Configure the standard library `logging` module to direct all log messages exclusively to `sys.stderr`. Never use bare `print()` in server execution paths.

### 2. Azure Authentication Hangs in Offline or Headless Environments
- **Pitfall**: `DefaultAzureCredential` attempts multiple token providers in sequence (Environment, Managed Identity, Azure CLI, Interactive Browser). If not properly configured or if running in an offline environment without credentials, it can hang or take minutes before timing out, stalling Claude Desktop tool execution.
- **Mitigation**: Implement a fast, defensive check for expected Azure environment variables (`AZURE_STORAGE_ACCOUNT_NAME`) or explicit short timeout wrapping. Immediately fall back to the embedded mock dataset when credentials or account configurations are missing, logging a clear warning to `stderr`.

### 3. Missing Storage Blob Data Reader RBAC Propagation
- **Pitfall**: In Azure, Storage Account Owner or Contributor role alone does NOT grant data-plane access to read blobs when Azure AD authentication is used. Deployments frequently fail with `403 AuthorizationPermissionMismatch`.
- **Mitigation**: Explicitly provision `azurerm_role_assignment` binding `Storage Blob Data Reader` to the Managed Identity on the Storage Account scope in Terraform.

### 4. Floating-Point Calculation Drift in FinOps Calculations
- **Pitfall**: Naive floating-point math in financial estimates can produce messy results like `$1234.5600000000002` or rounding discrepancies in itemized sums.
- **Mitigation**: Deterministically round all financial values to two decimal places (`round(val, 2)`) and format them with explicit commas and dollar signs (`${val:,.2f}`).

### 5. Windows vs Linux Path Delimiters in Claude Desktop Config
- **Pitfall**: On Windows machines, Windows backslashes in `claude_desktop_config.json` must be escaped (`C:\\path\\to\\python.exe`) or written with forward slashes (`C:/path/to/python.exe`), otherwise Claude Desktop fails to parse the config file.
- **Mitigation**: Provide clear instructions and examples in `README.md` and `claude_desktop_config.example.json` demonstrating cross-platform path formatting.

### 6. Missing Dependencies in Test Environments
- **Pitfall**: Tests that accidentally attempt live network calls to Azure Blob endpoints fail in CI or air-gapped developer workstations.
- **Mitigation**: Thoroughly mock `BlobServiceClient.from_connection_string` / `BlobServiceClient(account_url=...)` and the `download_blob().readall()` stream in `tests/test_server.py`.
