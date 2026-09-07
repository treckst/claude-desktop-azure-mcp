# Features Research: Cloud Telemetry & FinOps Modernization MCP

**Domain:** Enterprise Telemetry Inspection & FinOps Cost Estimation  
**Date:** 2026-09-07  
**Status:** Complete  

## Feature Matrix

| Feature | Category | Confidence | Description & Value Proposition |
|---|---|---|---|
| **`get_client_telemetry`** | Table Stakes | HIGH | Fetch workload metrics for a specific enterprise client ID (retail, fintech, logistics). Returns workload name, monthly DB queries, storage volume in TB, and current monthly cloud spend in USD. |
| **`calculate_modernization_tco`** | Differentiator | HIGH | Deterministic FinOps model calculating a 30% baseline infrastructure modernization reduction, plus monthly Claude Haiku token cost based on query volume, yielding net monthly projected savings. |
| **Resilient Mock Fallback** | Enterprise Reliability | HIGH | Automatic fallback to an embedded 3-record DataFrame when Azure credentials or network access are unavailable, emitting clear warning logs to stderr. |
| **Zero-Secret Identity Integration** | Security / Enterprise | HIGH | Seamless authentication via Azure Managed Identity and Azure CLI without credentials in files or command args. |
| **Claude Desktop Stdio Config** | Usability / Integration | HIGH | Ready-to-use JSON configuration snippet mapping Python virtual environment and environment variables for local Claude Desktop execution. |
| **Automated CI Validation** | Quality Assurance | HIGH | Continuous integration with Ruff linting and 100% offline Pytest test suite covering mock downloads, tool execution, and error handling. |

## Detailed Tool Specifications

### 1. `get_client_telemetry(client_id: str) -> str`
- **Inputs**: `client_id` (case-insensitive string matching, e.g., `CL-RETAIL-01`, `CL-FINTECH-02`, `CL-LOGISTICS-03`).
- **Telemetry Schema**:
  - `client_id`: Unique client identifier
  - `workload_name`: Application or service designation
  - `monthly_db_queries`: Integer count of queries executed per month
  - `storage_tb`: Floating point volume of active storage in Terabytes
  - `current_monthly_spend_usd`: Current baseline monthly infrastructure expenditure in USD
- **Output**: Clean, executive-ready textual summary formatted with clear headings, metric highlights, and currency formatting.
- **Error Handling**: When `client_id` is missing, returns descriptive error message with list of available client IDs rather than crashing.

### 2. `calculate_modernization_tco(current_spend_usd: float, estimated_ai_monthly_queries: int) -> str`
- **Inputs**:
  - `current_spend_usd`: Existing monthly spend (positive float)
  - `estimated_ai_monthly_queries`: Expected monthly AI workload volume (positive int)
- **Calculation Formulae**:
  - **Base Infrastructure Modernization Savings**: `30%` reduction on current spend (`current_spend_usd * 0.30`).
  - **Modernized Base Infra Cost**: `current_spend_usd * 0.70`.
  - **Anthropic Claude Haiku Sizing & Token Costs**:
    - Average tokens per query: 1,000 input tokens + 300 output tokens.
    - Claude 3 Haiku rates: $0.25 / M input tokens, $1.25 / M output tokens (blended ~$0.000625/query).
    - Monthly Token Cost = `estimated_ai_monthly_queries * ((1000/1e6)*0.25 + (300/1e6)*1.25)`.
  - **Total Modernized Monthly Cost**: `Modernized Base Infra Cost + Monthly Token Cost`.
  - **Net Projected Monthly Savings**: `current_spend_usd - Total Modernized Monthly Cost`.
- **Output**: Transparent, audit-ready itemized breakdown displaying Baseline Spend, Modernized Infrastructure Spend, Projected AI Token Cost, and Net Monthly Savings & ROI percentage.
