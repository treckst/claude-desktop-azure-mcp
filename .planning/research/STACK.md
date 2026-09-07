# Stack Research: MCP Azure Telemetry Bridge

**Domain:** Model Context Protocol (MCP) Server for Claude Desktop & Azure Blob Storage  
**Date:** 2026-09-07  
**Status:** Complete  

## Technology Stack

| Layer | Technology | Version / Spec | Confidence | Notes |
|---|---|---|---|---|
| **Protocol / Core** | Model Context Protocol (`mcp`) | `mcp[cli]>=1.0.0` | HIGH | Uses official Python SDK `mcp.server.fastmcp.FastMCP` |
| **Transport** | Stdio (Standard I/O) | Claude Desktop default | HIGH | Communicates over stdin/stdout with JSON-RPC; stderr reserved for logging |
| **Cloud Provider** | Microsoft Azure Storage | `azure-storage-blob>=12.19.0` | HIGH | BlobServiceClient, ContainerClient, BlobClient with chunked/streamed download |
| **Cloud Authentication**| Azure Identity | `azure-identity>=1.15.0` | HIGH | `DefaultAzureCredential` chained fallback (Environment -> Workload Identity -> Managed Identity -> Azure CLI -> Interactive) |
| **Data Engine** | Pandas | `pandas>=2.0.0` | HIGH | In-memory CSV parsing, filtering by `client_id`, deterministic math aggregations |
| **Infrastructure as Code**| Terraform | `azurerm ~> 3.0 or ~> 4.0` | HIGH | Declarative infrastructure for RG, Storage Account, Blob Container, Managed Identity, and RBAC |
| **Testing Framework** | Pytest + unittest.mock | `pytest>=8.0.0` | HIGH | Offline mock testing avoiding live Azure network roundtrips |
| **Linting & Quality** | Ruff | `ruff>=0.4.0` | HIGH | Modern, ultra-fast Python linter and formatter |
| **CI/CD Pipeline** | GitHub Actions | Ubuntu / Python 3.11 | HIGH | Automated checkout, dependency caching, Ruff check, and pytest run |

## Evaluation & Rationale

1. **Why `FastMCP` instead of low-level `Server` / `stdio_server`?**
   - Built-in type serialization, schema generation from Python docstrings and type annotations.
   - Clean decorator syntax (`@mcp.tool()`) reducing boilerplate and eliminating JSON schema drift.

2. **Why `DefaultAzureCredential`?**
   - Zero-credential hardcoding in local code or git.
   - Seamless workflow: Developers use `az login` locally; deployed workloads in Azure VMs/Containers use the User Assigned Managed Identity (`id-mcp-reader`).

3. **Why Stdio Transport?**
   - Native integration with Claude Desktop `claude_desktop_config.json`.
   - Isolates execution per session, lifecycle managed directly by Claude Desktop process.
