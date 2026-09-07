"""Comprehensive test suite for AzureTelemetryBridge MCP server.

Validates:
1. Resilient offline fallback and DefaultAzureCredential Azure Blob integration (mocked).
2. Case-insensitive client telemetry queries and error messages.
3. Deterministic mathematical accuracy of modernization TCO and Haiku token models.
4. Input validation and edge cases.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import server


class TestDataLoadingAndFallback:
    """Tests for Azure Blob data retrieval and fallback behaviors."""

    def test_mock_dataframe_structure(self):
        """Verify embedded mock DataFrame contains required enterprise columns and 3 records."""
        df = server.get_mock_dataframe()
        expected_columns = {
            "client_id",
            "workload_name",
            "industry",
            "monthly_db_queries",
            "storage_tb",
            "current_monthly_spend_usd",
            "active_vms",
            "estimated_ai_monthly_queries",
        }
        assert set(df.columns) == expected_columns
        assert len(df) == 3

        client_ids = set(df["client_id"].tolist())
        assert client_ids == {"RETAIL-001", "FINTECH-002", "LOGISTICS-003"}

    def test_fallback_when_storage_account_env_unset(self, monkeypatch):
        """When AZURE_STORAGE_ACCOUNT_NAME is not set, fallback returns mock data."""
        monkeypatch.delenv("AZURE_STORAGE_ACCOUNT_NAME", raising=False)
        df = server.load_telemetry_data()
        assert len(df) == 3
        assert "RETAIL-001" in df["client_id"].values

    def test_fallback_on_azure_exception(self, monkeypatch):
        """When Azure connection raises an exception, fallback returns mock data."""
        monkeypatch.setenv("AZURE_STORAGE_ACCOUNT_NAME", "teststorageacct")

        with patch("server.BlobServiceClient") as mock_blob_service:
            mock_blob_service.side_effect = RuntimeError("Azure network failure")
            df = server.load_telemetry_data()
            assert len(df) == 3
            assert "FINTECH-002" in df["client_id"].values

    def test_successful_azure_blob_download(self, monkeypatch):
        """When Azure Blob Storage succeeds, remote CSV records are loaded."""
        monkeypatch.setenv("AZURE_STORAGE_ACCOUNT_NAME", "teststorageacct")
        monkeypatch.setenv("AZURE_CONTAINER_NAME", "client-workloads")
        monkeypatch.setenv("AZURE_BLOB_NAME", "client_telemetry.csv")

        csv_content = (
            b"client_id,workload_name,industry,monthly_db_queries,storage_tb,"
            b"current_monthly_spend_usd,active_vms,estimated_ai_monthly_queries\n"
            b"REMOTE-999,Cloud Native AI Platform,Technology,50000000,100.0,500000.00,1000,200000\n"
        )

        mock_blob_client = MagicMock()
        mock_download_stream = MagicMock()
        mock_download_stream.readall.return_value = csv_content
        mock_blob_client.download_blob.return_value = mock_download_stream

        mock_service_instance = MagicMock()
        mock_service_instance.get_blob_client.return_value = mock_blob_client

        with (
            patch("server.BlobServiceClient", return_value=mock_service_instance),
            patch("server.DefaultAzureCredential"),
        ):
            df = server.load_telemetry_data()
            assert len(df) == 1
            assert df.iloc[0]["client_id"] == "REMOTE-999"
            assert df.iloc[0]["industry"] == "Technology"


class TestGetClientTelemetryTool:
    """Tests for the get_client_telemetry MCP tool."""

    def test_valid_client_id_lookup(self, monkeypatch):
        """Verify successful lookup returns formatted telemetry metrics."""
        monkeypatch.delenv("AZURE_STORAGE_ACCOUNT_NAME", raising=False)
        result = server.get_client_telemetry("RETAIL-001")

        assert "RETAIL-001" in result
        assert "Global Retail Omnichannel" in result
        assert "$125,000.00" in result
        assert "15.4 TB" in result
        assert "15,400,000" in result
        assert "240" in result

    def test_case_insensitive_matching(self, monkeypatch):
        """Verify case insensitivity and whitespace stripping."""
        monkeypatch.delenv("AZURE_STORAGE_ACCOUNT_NAME", raising=False)

        result_lower = server.get_client_telemetry("  fintech-002  ")
        assert "FINTECH-002" in result_lower
        assert "Apex Financial Services" in result_lower
        assert "$340,000.00" in result_lower

        result_mixed = server.get_client_telemetry("LoGiStIcS-003")
        assert "LOGISTICS-003" in result_mixed
        assert "Nexus Freight Logistics" in result_mixed

    def test_unknown_client_id_returns_friendly_error(self, monkeypatch):
        """Unknown ID returns available IDs in message."""
        monkeypatch.delenv("AZURE_STORAGE_ACCOUNT_NAME", raising=False)
        result = server.get_client_telemetry("UNKNOWN-999")

        assert "not found" in result
        assert "RETAIL-001" in result
        assert "FINTECH-002" in result
        assert "LOGISTICS-003" in result

    def test_empty_client_id_validation(self):
        """Empty or whitespace-only client_id returns an error message."""
        assert "Error: client_id parameter is required." in server.get_client_telemetry(
            ""
        )
        assert "Error: client_id parameter is required." in server.get_client_telemetry(
            "   "
        )


class TestCalculateModernizationTcoTool:
    """Tests for the calculate_modernization_tco MCP tool."""

    def test_deterministic_tco_calculation(self):
        """Verify accurate calculation of 30% reduction, Haiku costs, and net savings."""
        # Baseline spend: $100,000.00
        # AI queries: 50,000
        # Infra reduction: 30% -> $30,000 savings -> $70,000 modernized spend
        # Haiku cost: 50,000 * $0.001 = $50.00
        # Net monthly savings: $30,000 - $50 = $29,950.00
        # Annualized savings: $29,950 * 12 = $359,400.00
        # Net cost reduction ROI: 29.95% -> 30.0%
        result = server.calculate_modernization_tco(
            current_spend_usd=100000.0,
            estimated_ai_monthly_queries=50000,
        )

        assert "$100,000.00" in result
        assert "$70,000.00" in result
        assert "$30,000.00" in result
        assert "$50.00" in result
        assert "$70,050.00" in result
        assert "$29,950.00" in result
        assert "$359,400.00" in result
        assert "29.9%" in result or "30.0%" in result

    def test_zero_queries_scenario(self):
        """Verify TCO behavior when AI query count is zero."""
        result = server.calculate_modernization_tco(
            current_spend_usd=50000.0,
            estimated_ai_monthly_queries=0,
        )
        assert "$50,000.00" in result
        assert "$35,000.00" in result
        assert "$15,000.00" in result
        assert "$0.00" in result
        assert "30.0%" in result

    def test_negative_spend_validation(self):
        """Negative spend returns descriptive error."""
        result = server.calculate_modernization_tco(-1000.0, 1000)
        assert "Error: current_spend_usd cannot be negative." in result

    def test_negative_queries_validation(self):
        """Negative query count returns descriptive error."""
        result = server.calculate_modernization_tco(1000.0, -10)
        assert "Error: estimated_ai_monthly_queries cannot be negative." in result

    def test_zero_spend_handles_division(self):
        """Zero spend handles ROI calculation gracefully without ZeroDivisionError."""
        result = server.calculate_modernization_tco(0.0, 100)
        assert "0.0%" in result


class TestFastMCPRegistration:
    """Verify FastMCP tool registration."""

    def test_server_tools_registered(self):
        """Verify get_client_telemetry and calculate_modernization_tco are registered on mcp."""
        # FastMCP stores tools in its registry
        tool_names = [t.name for t in server.mcp._tool_manager.list_tools()]
        assert "get_client_telemetry" in tool_names
        assert "calculate_modernization_tco" in tool_names
