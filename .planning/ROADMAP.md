# Roadmap: Claude Desktop Azure Telemetry Bridge MCP

## Milestone 1: Enterprise Production Harness

### Progress

| Phase | Name | Status | Plans | Date |
|---|---|---|---|---|
| **Phase 1** | Foundation & Dependencies | Complete | 2 plans | 2026-09-07 |
| **Phase 2** | Terraform Cloud Infrastructure | Complete | 2 plans | 2026-09-07 |
| **Phase 3** | FastMCP Server & Modernization Tools | Complete | 2 plans | 2026-09-07 |
| **Phase 4** | Test Harness & GitHub Actions CI | Complete | 2 plans | 2026-09-07 |
| **Phase 5** | Claude Desktop Integration & Documentation | Complete | 2 plans | 2026-09-07 |

---

### Phases

#### Phase 1: Foundation & Dependencies
**Goal:** Establish clean repository foundations, dependency pinning, and environment hygiene.  
**Requirements:** R1.1  
- [x] Create `requirements.txt` with pinned dependencies (`mcp[cli]`, `azure-identity`, `azure-storage-blob`, `pandas`, `pytest`, `ruff`).
- [x] Create enterprise `.gitignore` covering Python cache, virtual environments, Terraform state/lock files, secrets, IDE, and OS artifacts.

#### Phase 2: Terraform Cloud Infrastructure
**Goal:** Provision secure, automated Azure storage and identity infrastructure with sample telemetry data.  
**Requirements:** R2.1, R2.2, R2.3, R2.4, R2.5  
- [x] Create `terraform/variables.tf` with customizable defaults (resource group name, location, storage account prefix, blob container name).
- [x] Create `terraform/client_telemetry.csv` with enterprise client seed dataset (retail, fintech, logistics).
- [x] Create `terraform/main.tf` declaring Resource Group, Storage Account (TLS 1.2, HNS disabled), Blob Container (`client-workloads`), Blob upload, User Assigned Managed Identity (`id-mcp-reader`), and `Storage Blob Data Reader` RBAC assignment.
- [x] Create `terraform/outputs.tf` exporting storage account name, container name, blob endpoint, and managed identity client ID.

#### Phase 3: FastMCP Server & Modernization Tools
**Goal:** Implement resilient FastMCP server with Azure Blob data loader, offline fallback, and deterministic FinOps tools.  
**Requirements:** R3.1, R3.2, R3.3, R3.4, R3.5  
- [x] Implement `server.py` with `mcp.server.fastmcp.FastMCP` instance `AzureTelemetryBridge`.
- [x] Implement Azure Blob client authentication with `DefaultAzureCredential` and automatic fallback to embedded 3-record DataFrame with stderr warnings.
- [x] Implement `get_client_telemetry(client_id: str)` tool with case-insensitive search and friendly formatting.
- [x] Implement `calculate_modernization_tco(current_spend_usd: float, estimated_ai_monthly_queries: int)` tool with 30% infra reduction and Claude Haiku token calculations.

#### Phase 4: Test Harness & GitHub Actions CI
**Goal:** Deliver 100% offline unit and integration test coverage and automated lint/test CI pipeline.  
**Requirements:** R4.1, R4.2  
- [x] Create `tests/__init__.py` and `tests/test_server.py`.
- [x] Implement tests mocking Azure Blob downloads via `unittest.mock` to verify offline functionality.
- [x] Test telemetry queries for valid IDs, missing IDs, and case insensitivity.
- [x] Test deterministic mathematical accuracy and edge cases of the TCO calculator.
- [x] Create `.github/workflows/ci.yml` running Python 3.11 setup, Ruff linting, and Pytest.

#### Phase 5: Claude Desktop Integration & Documentation
**Goal:** Provide turnkey configuration for Claude Desktop and clear architectural documentation.  
**Requirements:** R5.1, R5.2  
- [x] Create `claude_desktop_config.example.json` with stdio parameters and environment variable definitions.
- [x] Create comprehensive `README.md` detailing architecture, Terraform provisioning, local setup, testing, and Claude Desktop connection.
- [x] Run linting and test suite verification locally to ensure clean execution.

---
*Last updated: 2026-09-07*
