# Requirements: Claude Desktop Azure Telemetry Bridge MCP

## Overview
Functional and technical requirements for the **AzureTelemetryBridge** MCP server, cloud infrastructure, test harness, and Claude Desktop integration.

## V1 — Must Have

| ID | Requirement | Phase | Status |
|---|---|---|---|
| **R1.1** | Define project dependencies (`requirements.txt` with `mcp[cli]`, `azure-identity`, `azure-storage-blob`, `pandas`, `pytest`, `ruff`) and comprehensive `.gitignore` (Python, Terraform, IDE, OS). | Phase 1 | Complete |
| **R2.1** | Terraform Azure provider (`azurerm` version ~> 3.0 / 4.0) with configurable variables (`variables.tf`) and location defaults. | Phase 2 | Complete |
| **R2.2** | Terraform Resource Group (default: `rg-chaosgears-telemetry`) and Storage Account (Standard LRS, TLS 1.2, HNS disabled). | Phase 2 | Complete |
| **R2.3** | Terraform Blob Container `client-workloads` and sample CSV blob upload (`client_telemetry.csv`). | Phase 2 | Complete |
| **R2.4** | Terraform User Assigned Managed Identity (`id-mcp-reader`) and `Storage Blob Data Reader` role assignment scoped to the storage account. | Phase 2 | Complete |
| **R2.5** | Terraform outputs (`outputs.tf`) exposing storage account name, blob container name, primary blob endpoint, and managed identity client ID. | Phase 2 | Complete |
| **R3.1** | FastMCP server definition named `AzureTelemetryBridge` using `mcp.server.fastmcp.FastMCP` over Stdio transport with stderr logging. | Phase 3 | Complete |
| **R3.2** | Azure authentication and blob retrieval via `azure.identity.DefaultAzureCredential` and `azure-storage-blob` reading remote CSV data. | Phase 3 | Complete |
| **R3.3** | Embedded mock fallback DataFrame with 3 realistic enterprise client records (retail, fintech, logistics) with columns: `client_id`, `workload_name`, `monthly_db_queries`, `storage_tb`, `current_monthly_spend_usd`, logging clear warnings when falling back. | Phase 3 | Complete |
| **R3.4** | Tool: `get_client_telemetry(client_id: str)` returning formatted textual telemetry metrics with case-insensitive search and friendly missing-ID error handling. | Phase 3 | Complete |
| **R3.5** | Tool: `calculate_modernization_tco(current_spend_usd: float, estimated_ai_monthly_queries: int)` computing 30% base infrastructure modernization reduction, Claude Haiku token costs, and net projected monthly savings with itemized audit breakdown. | Phase 3 | Complete |
| **R4.1** | Pytest test suite (`tests/test_server.py`) with `unittest.mock` covering offline operations, remote blob download mocks, mock fallback trigger, telemetry queries, invalid IDs, and mathematical accuracy of TCO calculations. | Phase 4 | Complete |
| **R4.2** | GitHub Actions CI workflow (`.github/workflows/ci.yml`) triggering on push and pull requests to `main`, setting up Python 3.11, running Ruff linting, and executing Pytest. | Phase 4 | Complete |
| **R5.1** | `claude_desktop_config.example.json` demonstrating stdio registration with Claude Desktop passing `AZURE_STORAGE_ACCOUNT_NAME`. | Phase 5 | Complete |
| **R5.2** | Executive and technical `README.md` with end-to-end instructions for Terraform deployment, local environment setup, offline mock testing, and Claude Desktop connection. | Phase 5 | Complete |

## V2 — Nice to Have (Post-V1 Enhancements)

| ID | Requirement | Priority | Status |
|---|---|---|---|
| **R6.1** | Multi-cloud storage adapters (AWS S3, GCP Cloud Storage) for multi-cloud workload assessments. | Low | Backlog |
| **R6.2** | Support for custom LLM model selection in TCO calculations (e.g., Claude 3.5 Sonnet vs Haiku). | Medium | Backlog |
| **R6.3** | Dynamic blob telemetry refresh / cache-busting tool for live cloud updates. | Medium | Backlog |

## Out of Scope
- Write/update/delete operations against client telemetry in Azure Blob Storage.
- Web or SSE remote network transport for Claude Desktop (v1 strictly stdio).
- Direct Azure billing API integration (telemetry is ingested via CSV dataset).

---
*Last updated: 2026-09-07*
