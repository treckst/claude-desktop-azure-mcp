# Architecture Research: Azure Telemetry Bridge MCP

**Domain:** Claude Desktop MCP Server & Azure Cloud Telemetry Architecture  
**Date:** 2026-09-07  
**Status:** Complete  

## System Architecture Diagram

```mermaid
flowchart TD
    subgraph Local Environment [User Workstation / Claude Desktop]
        CD[Claude Desktop Client]
        CONFIG[claude_desktop_config.json]
        CD -->|Spawns via Stdio JSON-RPC| MCP[FastMCP Server: AzureTelemetryBridge]
    end

    subgraph MCP Server Internals [server.py]
        MCP --> ROUTER[FastMCP Tool Router]
        ROUTER --> TOOL1[get_client_telemetry]
        ROUTER --> TOOL2[calculate_modernization_tco]
        
        TOOL1 --> DATA_LAYER[Telemetry Data Loader]
        DATA_LAYER -->|1. Try Cloud Fetch| AZ_CLIENT[BlobServiceClient / ContainerClient]
        DATA_LAYER -.->|2. Fallback on Error| MOCK_DF[Embedded Enterprise Mock DataFrame]
    end

    subgraph Azure Cloud [Azure Commercial Cloud]
        AZ_AUTH[DefaultAzureCredential]
        STORAGE_ACCT[(Storage Account: rg-chaosgears-telemetry)]
        CONTAINER[Container: client-workloads]
        BLOB[Blob: client_telemetry.csv]
        MI[Managed Identity: id-mcp-reader]
        
        AZ_CLIENT --> AZ_AUTH
        AZ_AUTH -->|OAuth Token / RBAC| STORAGE_ACCT
        STORAGE_ACCT --> CONTAINER
        CONTAINER --> BLOB
        MI -.->|Role: Storage Blob Data Reader| STORAGE_ACCT
    end
```

## Component Breakdown

1. **Claude Desktop Integration Layer (`claude_desktop_config.json`)**:
   - Spawns Python virtual environment interpreter executing `server.py`.
   - Injects environment variables (`AZURE_STORAGE_ACCOUNT_NAME`, `AZURE_STORAGE_CONTAINER_NAME`, `AZURE_STORAGE_BLOB_NAME`).
   - JSON-RPC communication strictly over `sys.stdin` and `sys.stdout`.

2. **Server & Tool Core (`server.py`)**:
   - Built on `mcp.server.fastmcp.FastMCP`.
   - Logging routed strictly to `sys.stderr` (ensures `sys.stdout` remains pristine JSON-RPC).
   - In-memory caching/singleton data loader to avoid redundant downloads on every query.
   - Robust DataFrame validation with column types: `client_id` (str), `workload_name` (str), `monthly_db_queries` (int), `storage_tb` (float), `current_monthly_spend_usd` (float).

3. **Cloud Infrastructure Layer (`terraform/`)**:
   - Resource Group: `rg-chaosgears-telemetry` (configurable via variables).
   - Storage Account: Secure baseline (`account_tier = "Standard"`, `account_replication_type = "LRS"`, `min_tls_version = "TLS1_2"`, `is_hns_enabled = false`).
   - Blob Container: `client-workloads` (`container_access_type = "private"`).
   - Blob: `client_telemetry.csv` populated with initial client telemetry dataset.
   - Identity & RBAC: `azurerm_user_assigned_identity` (`id-mcp-reader`) assigned `Storage Blob Data Reader` role on the storage account scope.
   - Clean Terraform outputs exposing storage account name, blob container name, primary blob endpoint, and identity client ID.

4. **Testing & CI Pipeline (`tests/test_server.py`, `.github/workflows/ci.yml`)**:
   - Pytest suite using `unittest.mock.patch` for `BlobServiceClient` and `DefaultAzureCredential`.
   - Tests run completely offline and verify fallback behavior, valid client queries, invalid client ID handling, and deterministic mathematical accuracy of the TCO calculator.
   - GitHub Actions CI matrix executing Ruff linting and pytest under Python 3.11.
