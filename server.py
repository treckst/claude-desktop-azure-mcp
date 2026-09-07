"""Azure Telemetry Bridge MCP Server.

Provides Claude Desktop with direct Model Context Protocol (MCP) access to
enterprise cloud client telemetry stored in Azure Blob Storage, along with
deterministic cloud modernization Total Cost of Ownership (TCO) calculators.
"""

from __future__ import annotations

import io
import logging
import os
import sys
from typing import Any

import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from mcp.server.fastmcp import FastMCP

# Configure logging strictly to sys.stderr to prevent stdout JSON-RPC transport corruption
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("AzureTelemetryBridge")

# Embedded enterprise mock dataset (3 verticals: Retail, FinTech, Logistics)
MOCK_TELEMETRY_DATA: dict[str, list[Any]] = {
    "client_id": ["RETAIL-001", "FINTECH-002", "LOGISTICS-003"],
    "workload_name": [
        "Global Retail Omnichannel",
        "Apex Financial Services",
        "Nexus Freight Logistics",
    ],
    "industry": [
        "Retail & E-commerce",
        "Banking & Capital Markets",
        "Supply Chain & Transportation",
    ],
    "monthly_db_queries": [15400000, 42000000, 9800000],
    "storage_tb": [15.4, 42.0, 9.8],
    "current_monthly_spend_usd": [125000.00, 340000.00, 89000.00],
    "active_vms": [240, 580, 160],
    "estimated_ai_monthly_queries": [45000, 120000, 25000],
}


def get_mock_dataframe() -> pd.DataFrame:
    """Return an in-memory copy of the 3-record enterprise mock DataFrame."""
    return pd.DataFrame(MOCK_TELEMETRY_DATA)


def load_telemetry_data() -> pd.DataFrame:
    """Load telemetry dataset from Azure Blob Storage with graceful fallback to mock data.

    Attempts connection using DefaultAzureCredential against the configured Azure
    storage account and container. If environment variables are missing, credentials
    fail, or the blob cannot be downloaded, a warning is logged to stderr and the
    embedded 3-record enterprise mock DataFrame is returned.
    """
    storage_account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    container_name = os.getenv("AZURE_CONTAINER_NAME", "client-workloads")
    blob_name = os.getenv("AZURE_BLOB_NAME", "client_telemetry.csv")

    if not storage_account_name:
        logger.warning(
            "AZURE_STORAGE_ACCOUNT_NAME environment variable not set. "
            "Falling back to embedded 3-record mock enterprise dataset."
        )
        return get_mock_dataframe()

    try:
        account_url = f"https://{storage_account_name}.blob.core.windows.net"
        logger.info(
            "Attempting to download %s/%s from %s using DefaultAzureCredential...",
            container_name,
            blob_name,
            account_url,
        )

        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(
            account_url=account_url, credential=credential
        )
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )

        stream = blob_client.download_blob()
        raw_bytes = stream.readall()
        df = pd.read_csv(io.BytesIO(raw_bytes))
        logger.info(
            "Successfully loaded %d client telemetry records from Azure Blob Storage.",
            len(df),
        )
        return df

    except Exception as exc:  # noqa: BLE001 - Resilient fallback requires catching any unexpected runtime/Azure errors
        logger.warning(
            "Failed to retrieve telemetry from Azure Blob Storage (%s). "
            "Falling back to embedded 3-record mock enterprise dataset.",
            exc,
        )
        return get_mock_dataframe()


# Initialize FastMCP Server instance
mcp = FastMCP("AzureTelemetryBridge")


@mcp.tool()
def get_client_telemetry(client_id: str) -> str:
    """Retrieve client telemetry and cloud workload metrics.

    Searches Azure Blob Storage (or fallback mock catalog) using case-insensitive
    matching. Returns current monthly spend, storage volume, query throughput,
    and active virtual machines.

    Args:
        client_id: Unique enterprise client ID (e.g., 'RETAIL-001', 'FINTECH-002', 'LOGISTICS-003'). Case-insensitive.

    Returns:
        Structured Markdown telemetry report, or a friendly error listing available client IDs.
    """
    if not client_id or not client_id.strip():
        return "Error: client_id parameter is required."

    df = load_telemetry_data()
    clean_id = client_id.strip().upper()

    matched = df[df["client_id"].astype(str).str.strip().str.upper() == clean_id]

    if matched.empty:
        available_ids = ", ".join(df["client_id"].astype(str).tolist())
        return (
            f"Client ID '{client_id.strip()}' not found in telemetry store.\n\n"
            f"Available client IDs: {available_ids}"
        )

    row = matched.iloc[0]

    report = (
        f"### 📊 Telemetry Profile: {row['client_id']} — {row['workload_name']}\n\n"
        f"- **Industry Vertical:** {row['industry']}\n"
        f"- **Current Monthly Cloud Spend:** ${float(row['current_monthly_spend_usd']):,.2f}\n"
        f"- **Workload Storage Volume:** {float(row['storage_tb']):,.1f} TB\n"
        f"- **Monthly Database Queries:** {int(row['monthly_db_queries']):,}\n"
        f"- **Active Virtual Machines:** {int(row['active_vms']):,}\n"
        f"- **Estimated AI Reasoning Queries (Monthly):** {int(row['estimated_ai_monthly_queries']):,}\n"
    )
    return report


@mcp.tool()
def calculate_modernization_tco(
    current_spend_usd: float,
    estimated_ai_monthly_queries: int,
) -> str:
    """Calculate modernization Total Cost of Ownership (TCO) and Claude Haiku migration economics.

    Evaluates a 30% baseline infrastructure cost reduction via cloud modernization
    (containerization, serverless refactoring, automated blob lifecycle tiering)
    coupled with high-throughput Anthropic Claude Haiku reasoning queries.

    Pricing Model:
      - Infrastructure Optimization: 30% reduction on current cloud spend
      - Claude Haiku Pricing: $0.25 / MTok input, $1.25 / MTok output
      - Workload Sizing: 1,500 input tokens ($0.000375) + 500 output tokens ($0.000625) = $0.001000 per query

    Args:
        current_spend_usd: Current monthly cloud spend in USD. Must be greater than or equal to 0.
        estimated_ai_monthly_queries: Projected monthly AI audit/reasoning queries. Must be greater than or equal to 0.

    Returns:
        Audit-ready modernization FinOps report with line-item breakdown, net monthly savings, and ROI projections.
    """
    if current_spend_usd < 0:
        return "Error: current_spend_usd cannot be negative."

    if estimated_ai_monthly_queries < 0:
        return "Error: estimated_ai_monthly_queries cannot be negative."

    # 1. Base Infrastructure Optimization (30% reduction)
    infra_reduction_rate = 0.30
    infra_savings_usd = current_spend_usd * infra_reduction_rate
    modernized_infra_spend_usd = current_spend_usd - infra_savings_usd

    # 2. Claude Haiku Token Economics ($0.001000 per query)
    cost_per_query_usd = 0.001000
    monthly_ai_token_spend_usd = estimated_ai_monthly_queries * cost_per_query_usd

    # 3. Net Modernization Economics
    projected_total_monthly_spend_usd = (
        modernized_infra_spend_usd + monthly_ai_token_spend_usd
    )
    net_monthly_savings_usd = current_spend_usd - projected_total_monthly_spend_usd
    annual_projected_savings_usd = net_monthly_savings_usd * 12.0

    savings_percentage = (
        (net_monthly_savings_usd / current_spend_usd * 100.0)
        if current_spend_usd > 0
        else 0.0
    )

    result = (
        "## ☁️ Cloud Modernization & AI TCO Assessment\n\n"
        "### 1. Baseline Workload Inputs\n"
        f"- **Current Monthly Cloud Spend:** ${current_spend_usd:,.2f}\n"
        f"- **Projected Monthly AI Queries:** {estimated_ai_monthly_queries:,}\n\n"
        "### 2. Modernized Infrastructure Sizing (30% Efficiency Gain)\n"
        f"- **Modernized Monthly Infra Spend:** ${modernized_infra_spend_usd:,.2f}\n"
        f"- **Gross Monthly Infra Savings:** ${infra_savings_usd:,.2f}\n\n"
        "### 3. Anthropic Claude Haiku Token Economics\n"
        "- **Model:** Claude 3.5 Haiku ($0.25/M input tokens, $1.25/M output tokens)\n"
        "- **Per-Query Profile:** 1,500 input tokens + 500 output tokens\n"
        f"- **Unit Cost per Query:** ${cost_per_query_usd:.6f}\n"
        f"- **Monthly AI Reasoning Cost:** ${monthly_ai_token_spend_usd:,.2f}\n\n"
        "### 4. Executive FinOps Summary\n"
        f"- **Projected Net Monthly Spend:** ${projected_total_monthly_spend_usd:,.2f}\n"
        f"- **Net Projected Monthly Savings:** ${net_monthly_savings_usd:,.2f}\n"
        f"- **Annualized Projected Savings:** ${annual_projected_savings_usd:,.2f}\n"
        f"- **Net Cost Reduction (ROI):** {savings_percentage:.1f}%\n"
    )
    return result


if __name__ == "__main__":
    logger.info("Initializing AzureTelemetryBridge FastMCP server over stdio...")
    mcp.run(transport="stdio")
