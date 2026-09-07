# Project: Claude Desktop Azure Telemetry Bridge MCP Server 🌉

## Vision
Build an end-to-end, enterprise-ready repository for an internal AI harness that integrates Claude Desktop with Azure data storage using the Model Context Protocol (MCP). Chaos Gears (an AWS & Anthropic partner) needs internal tools to streamline client cloud modernization evaluations for their Alliances and Sales team by enabling Claude Desktop to securely pull client telemetry stored in Azure Blob Storage and compute deterministic infrastructure modernization and LLM token migration costs.

## Core Value
Deterministic, secure, and resilient data bridging: Claude Desktop can reliably query client cloud telemetry from Azure Blob Storage (with graceful offline fallback) and compute transparent, audit-ready modernization TCO and Claude Haiku token migration models.

## Target Users
- **Chaos Gears Alliances & Sales Team**: Evaluating prospective and existing enterprise cloud migration accounts.
- **Solutions Architects & FinOps Specialists**: Modeling workload migrations, cost optimizations, and AI integration sizing.
- **Claude Desktop Users**: Running local generative reasoning while querying enterprise data stores via MCP.

## Technical Context
- **MCP Framework**: Python `mcp.server.fastmcp.FastMCP` ("AzureTelemetryBridge") over `stdio`. [USER-chosen]
- **Cloud Infrastructure**: Azure Resource Group, Storage Account (LRS, TLS 1.2, HNS disabled), Blob Container (`client-workloads`), sample telemetry CSV (`client_telemetry.csv`), User Assigned Managed Identity (`id-mcp-reader`), and Role Assignment (`Storage Blob Data Reader`). [USER-chosen]
- **IaC**: Terraform with `azurerm` provider (~> 3.0 / 4.0). [USER-chosen]
- **Authentication**: `azure.identity.DefaultAzureCredential` (supports local Azure CLI, environment variables, and Azure Managed Identity without hardcoded credentials). [USER-chosen]
- **Data Engine**: Pandas for CSV parsing, filtering, and metric calculation. [USER-chosen]
- **Resilience / Fallback**: Automatic detection and graceful fallback to embedded 3-record enterprise client mock dataset (retail, fintech, logistics) when Azure credentials or connectivity are unavailable. [USER-chosen]
- **Quality & Automation**: Pytest suite with `unittest.mock` for offline testing, Ruff for linting, and GitHub Actions CI workflow targeting Python 3.11. [USER-chosen]

## Requirements

### Validated
(None yet — ship to validate)

### Active
- [x] **R1 (IaC)**: Terraform definitions in `terraform/` deploying Resource Group, Storage Account, Blob Container, Managed Identity, Role Assignment, and telemetry CSV upload with structured outputs.
- [x] **R2 (MCP Server)**: `server.py` implementing FastMCP server `AzureTelemetryBridge` with `get_client_telemetry` and `calculate_modernization_tco` tools.
- [x] **R3 (Auth & Storage)**: `DefaultAzureCredential` integration with `azure-storage-blob` client and fallback mechanism.
- [x] **R4 (Mock Fallback)**: Embedded 3-record enterprise DataFrame (retail, fintech, logistics) logging warnings on fallback.
- [x] **R5 (TCO Calculator)**: Deterministic TCO tool computing 30% base infra modernization reduction, monthly Claude Haiku token costs, and net projected monthly savings.
- [x] **R6 (Dependencies)**: `requirements.txt` specifying `mcp[cli]`, `azure-identity`, `azure-storage-blob`, `pandas`, `pytest`, `ruff`.
- [x] **R7 (Test Suite)**: Comprehensive Pytest suite in `tests/test_server.py` mocking Azure Blob operations and validating tools, errors, and calculations.
- [x] **R8 (CI/CD)**: GitHub Actions workflow in `.github/workflows/ci.yml` running linting (Ruff) and tests on push/PR to `main`.
- [x] **R9 (Config & Docs)**: `claude_desktop_config.example.json` and production-ready `README.md` with Terraform, Python, and Claude Desktop connection guide.

### Out of Scope
- Direct write/mutate operations back to Azure Blob Storage (read-only audit/analysis in v1).
- Multi-cloud AWS/GCP storage connectors in this initial Azure bridge repository.
- Public web/REST API gateway (server operates locally via stdio protocol for Claude Desktop).

## Key Decisions

| Decision | Source | Rationale | Outcome |
|----------|--------|-----------|---------|
| FastMCP (`mcp.server.fastmcp`) | User | Clean, ergonomic, standard Python MCP framework | Decided |
| `DefaultAzureCredential` | User | Zero-secret management, works across local Azure CLI and deployed Managed Identity | Decided |
| Embedded mock fallback | User | Guarantees developer experience and testing capability even when offline or without active Azure subscription | Decided |
| Haiku token pricing model | User | Balances high-throughput enterprise reasoning with deterministic unit economics | Decided |
| Terraform `azurerm` (~> 3.0 / 4.0) | User | Industry standard declarative cloud provisioning | Decided |

---
*Last updated: 2026-09-07 after initialization*
