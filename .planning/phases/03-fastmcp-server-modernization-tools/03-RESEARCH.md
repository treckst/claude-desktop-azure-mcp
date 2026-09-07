# Phase 3: FastMCP Server & Modernization Tools — Research

## Implementation Approach
Phase 3 builds the core application logic: the **AzureTelemetryBridge** MCP server in `server.py`. The server exposes two high-impact FinOps tools to Claude Desktop over the standardized Model Context Protocol (`stdio` transport):

1. **FastMCP Server Framework (`mcp.server.fastmcp`)**:
   - Pinned to MCP v1 line (`mcp[cli]>=1.3.0,<2.0.0`), utilizing the ergonomic decorator API:
     ```python
     from mcp.server.fastmcp import FastMCP

     mcp = FastMCP("AzureTelemetryBridge")
     ```
   - All diagnostic, debugging, and warning logs are strictly routed to `sys.stderr`. Writing to `sys.stdout` will break JSON-RPC communication with Claude Desktop.

2. **Azure Storage & Resilient Mock Fallback**:
   - Uses `azure.identity.DefaultAzureCredential` paired with `azure.storage.blob.BlobServiceClient`.
   - Supports zero-secret operation across local Azure CLI sessions and production User-Assigned Managed Identity.
   - If `AZURE_STORAGE_ACCOUNT_NAME` is unset or credentials/network connections are unavailable, it logs a clear warning to `sys.stderr` and returns an embedded 3-record Pandas DataFrame matching enterprise verticals:
     - Retail (`RETAIL-001`, Global Retail Omnichannel)
     - FinTech (`FINTECH-002`, Apex Financial Services)
     - Logistics (`LOGISTICS-003`, Nexus Freight Logistics)

3. **Tool 1: `get_client_telemetry(client_id: str) -> str`**:
   - Implements case-insensitive lookup (`client_id.strip().upper()`).
   - If found: returns a structured, human-readable summary of cloud spend, storage volume, database queries, active VMs, and AI queries.
   - If not found: provides a helpful error message enumerating available client IDs in the dataset.

4. **Tool 2: `calculate_modernization_tco(current_spend_usd: float, estimated_ai_monthly_queries: int) -> str`**:
   - Deterministic mathematical modeling for cloud modernization and Claude Haiku migration.
   - **Infrastructure Modernization**: 30% baseline savings via serverless, rightsizing, and blob tiering (`current_spend_usd * 0.30`).
   - **Claude Haiku Token Sizing**:
     - Model: Anthropic Claude 3 / 3.5 Haiku rates ($0.25 / MTok input, $1.25 / MTok output).
     - Standard FinOps workload profile: 1,500 input tokens + 500 output tokens per query ($0.001 per query).
   - Computes: Net monthly spend, Net monthly savings, Annualized projected savings, and ROI percentage.
   - Formats results into an audit-ready executive breakdown.

## Verification & Quality
- Stdio isolation: zero prints to stdout.
- Defensive typing with full type hints and docstrings.
- Ruff linting and formatting compliance.

---
*Researched: 2026-09-07*
