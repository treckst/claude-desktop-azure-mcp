# Phase 4: Test Harness & GitHub Actions CI — Research

## Implementation Approach
Phase 4 provides the enterprise quality gate for **AzureTelemetryBridge**:

1. **Deterministic Test Isolation with `unittest.mock`**:
   - Tests must run 100% offline without requiring an active Azure subscription, network access, or credentials.
   - Using `unittest.mock.patch`, we mock `server.BlobServiceClient` and `server.DefaultAzureCredential`.
   - Comprehensive test assertions validate:
     - Embedded DataFrame columns and 3 seed records.
     - Unset environment variable fallback.
     - Azure exception fallback.
     - Successful mocked remote blob download.
     - Valid and case-insensitive client telemetry lookups.
     - Helpful error messages for unknown client IDs.
     - Mathematical accuracy of TCO (30% infra reduction and Haiku per-query token modeling).
     - Input boundary conditions (negative values, zero spend).
     - FastMCP tool registry verification.

2. **Automated CI/CD Pipeline (`.github/workflows/ci.yml`)**:
   - Triggers on push and pull requests across `main`, `master`, and `gsd-super/**`.
   - Targets Python 3.11 runtime on `ubuntu-latest`.
   - Caches pip packages for fast execution.
   - Steps:
     - Linting: `ruff check .`
     - Code formatting: `ruff format --check .`
     - Unit test execution: `pytest -v tests/`

## Confidence & References
- Pytest standard assertion framework.
- GitHub Actions `setup-python@v5` with pip caching.
- Ruff ultra-fast linting and formatting.

---
*Researched: 2026-09-07*
