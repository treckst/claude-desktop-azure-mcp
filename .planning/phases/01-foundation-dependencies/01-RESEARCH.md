# Phase 1: Foundation & Dependencies — Research

## Implementation Approach
Phase 1 establishes the bedrock for the **AzureTelemetryBridge** MCP server project. This involves setting up clean, reproducible dependency management via `requirements.txt` and an enterprise-grade `.gitignore` that prevents secret leakage, Terraform state collisions, and platform-specific artifacts.

To ensure consistency across local development, offline CI workflows, and future Claude Desktop runs:
1. Pinned dependencies must account for the recent MCP Python SDK v2 release line (`mcp` 2.x), which restructured `FastMCP` into `MCPServer`. By pinning `mcp[cli]>=1.2.0,<2` (or `mcp[cli]~=1.3.0`), we preserve the exact `from mcp.server.fastmcp import FastMCP` API specified in the architectural requirements while maintaining full stability and Claude Desktop compatibility.
2. Azure SDK dependencies (`azure-identity` and `azure-storage-blob`) are pinned to production-stable releases that support `DefaultAzureCredential` and streaming Blob downloads without credential leaks.
3. Quality and testing tools (`ruff`, `pytest`) are pinned to modern versions aligned with Python 3.11+.
4. The `.gitignore` must comprehensively protect against Python bytecode/virtual environments, Terraform runtime cache/secrets (`.tfstate`, `*.tfvars`), and OS/IDE clutter across Windows, macOS, and Linux.

## Libraries & Tools
| Library | Purpose | Why | Confidence | Source |
|---------|---------|-----|-----------|--------|
| `mcp[cli]` (>=1.3.0,<2.0.0) | Model Context Protocol SDK & CLI | Provides `FastMCP` decorator API (`from mcp.server.fastmcp import FastMCP`) and inspector CLI | HIGH | [PyPI: mcp](https://pypi.org/project/mcp/) & [Migration Guide](https://py.sdk.modelcontextprotocol.io/migration/) |
| `azure-identity` (>=1.15.0, <=1.26.0) | Azure Microsoft Entra ID Authentication | Provides `DefaultAzureCredential` with zero-secret credential chain | HIGH | [PyPI: azure-identity](https://pypi.org/project/azure-identity/) |
| `azure-storage-blob` (>=12.19.0, <=12.31.0) | Azure Blob Storage Client | Provides `BlobServiceClient` for secure streaming download of CSV telemetry | HIGH | [PyPI: azure-storage-blob](https://pypi.org/project/azure-storage-blob/) |
| `pandas` (>=2.0.0, <3.1.0) | Data processing & tabular filtering | Parses telemetry CSV and performs deterministic client metric lookups | HIGH | [PyPI: pandas](https://pypi.org/project/pandas/) |
| `pytest` (>=8.0.0) | Unit & Integration testing framework | Executes test suite with assertion rewrites and mock isolation | HIGH | [PyPI: pytest](https://pypi.org/project/pytest/) |
| `ruff` (>=0.4.0) | High-performance Python linter & formatter | Ensures PEP 8 hygiene and catches syntax/import issues instantly | HIGH | [PyPI: ruff](https://pypi.org/project/ruff/) |

## Patterns to Follow
- **Conservative Upper Bounds for FastMCP**: `mcp[cli]>=1.3.0,<2.0.0` ensures backward-compatible FastMCP module imports without runtime breakage from MCP v2 SDK refactoring.
- **Hierarchical .gitignore Categorization**: Group rules logically (Python artifacts, Virtual environments, Testing/coverage caches, Terraform secrets and state, IDE settings, and OS temporary files).
- **Explicit Secret Exclusions**: Specifically ignore `.env`, `*.tfvars`, `*.tfvars.json`, `*.pem`, and `*.key` to prevent accidental commits of Azure credentials.

## Pitfalls to Avoid
- **Unconstrained `mcp` dependency**: Installing unpinned `mcp` would pull v2.x, which refactored `FastMCP` to `MCPServer`, breaking standard `from mcp.server.fastmcp import FastMCP` imports. Keeping `<2.0.0` guarantees stability.
- **Committing Terraform State**: Committing `.tfstate` files can leak sensitive infrastructure metadata and Azure resource IDs; ignore both local `.tfstate` and `.terraform/` plugins.
- **Platform-Specific Virtual Environment Names**: Developers use `.venv`, `venv`, or `env`; all must be ignored.

## Key References
- Model Context Protocol Python SDK: https://py.sdk.modelcontextprotocol.io/
- PyPI MCP Package Metadata: https://pypi.org/pypi/mcp/json
- Azure Identity Client Library: https://pypi.org/project/azure-identity/
- Azure Storage Blobs Client Library: https://pypi.org/project/azure-storage-blob/

## Unverified Claims
None. All package names, latest releases, and import paths were verified against live PyPI JSON feeds and official migration documentation.

---
*Researched: 2026-09-07*
