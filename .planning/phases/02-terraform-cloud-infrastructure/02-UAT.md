# Phase 2: Terraform Cloud Infrastructure — UAT

## Acceptance Criteria

1. **Declarative Cloud IaC**: `terraform/main.tf` defines Resource Group, Storage Account, Container, Blob, Managed Identity, and RBAC role assignment.
2. **Deterministic Inputs/Outputs**: `terraform/variables.tf` and `terraform/outputs.tf` export cloud connection parameters for Claude Desktop.
3. **Seed Telemetry**: `terraform/client_telemetry.csv` provides realistic client data.
4. **Validation**: `terraform validate` reports successful syntax.

## Result
ALL ACCEPTANCE CRITERIA MET. 4/4 passed.
