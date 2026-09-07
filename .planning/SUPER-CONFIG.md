# GSD SUPER ► CONFIGURATION LOCKED ⚡

Project:      Claude Desktop Azure Telemetry Bridge MCP Server
Branch:       gsd-super/azure-telemetry-bridge
Mode:         A — FULL AUTONOMY (End-to-end execution of Phases 2-5)
Approval:     1 — AI decides (Roadmap validated in .planning/ROADMAP.md)
Testing:      B — AUTOMATED (pytest test suite + ruff linting)
Stack:        Python 3.11+, FastMCP, Azure Blob Storage SDK, Azure Identity, Pandas, Terraform (azurerm)
Database:     Azure Blob Storage (`client_telemetry.csv` in container `client-workloads`) + 3-record offline fallback
Auth:         DefaultAzureCredential (zero-secret architecture)
UI:           FastMCP stdio interface for Claude Desktop
Deploy to:    Local Claude Desktop stdio bridge + Terraform Azure cloud definitions + GitHub Actions CI
Quality:      2 — PRODUCTION (Comprehensive offline tests, strict typing, error handling, CI/CD, and docs)

⚡ Starting autonomous execution. Running Phases 2, 3, 4, and 5 to completion.
