# Phase 2: Terraform Cloud Infrastructure — Research

## Implementation Approach
Phase 2 provisions the Azure cloud infrastructure and seed dataset required for the **AzureTelemetryBridge** MCP server. Using declarative Infrastructure as Code (IaC) via HashiCorp Terraform and the `azurerm` provider, we define a secure, least-privilege cloud environment:

1. **Customizable Variables (`variables.tf`)**:
   - Provide enterprise-ready defaults for Resource Group name (`rg-claude-telemetry-bridge`), Azure Region (`eastus`), Storage Account name prefix (`claudetel`), and Blob Container name (`client-workloads`).
   - Use `random_string` or `random_id` to generate globally unique, valid Azure Storage Account names (lowercase alphanumeric, 3-24 characters).

2. **Enterprise Client Telemetry Seed Dataset (`client_telemetry.csv`)**:
   - Seed data representing three major verticals: Retail (`RETAIL-001`), FinTech (`FINTECH-002`), and Logistics (`LOGISTICS-003`).
   - Columns: `client_id`, `client_name`, `industry`, `monthly_cloud_spend_usd`, `primary_workload`, `data_volume_gb`, `active_vms`, `estimated_ai_monthly_queries`.
   - Used for both direct cloud upload via Terraform and offline mock fallback in the MCP server.

3. **Secure Azure Storage & Identity (`main.tf`)**:
   - Enforce TLS 1.2 minimum (`min_tls_version = "TLS1_2"`).
   - Disable Hierarchical Namespace (`is_hns_enabled = false`) for standard Flat Blob storage.
   - Private container access (`container_access_type = "private"`).
   - User Assigned Managed Identity (`id-mcp-reader`) coupled with an explicit RBAC role assignment: `Storage Blob Data Reader` (`ba92f5b4-2d11-453d-a403-e96b0029c9fe` or role definition name `"Storage Blob Data Reader"`).
   - Direct provisioning of `azurerm_storage_blob` uploading `client_telemetry.csv` with content MD5 hashing for idempotent drift detection.

4. **Structured Outputs (`outputs.tf`)**:
   - Export `storage_account_name`, `storage_container_name`, `blob_endpoint`, `managed_identity_client_id`, and `telemetry_blob_name`.
   - These outputs plug directly into Claude Desktop runtime environment variables (`AZURE_STORAGE_ACCOUNT_NAME`, `AZURE_CONTAINER_NAME`, etc.).

## Libraries & Tools
| Tool / Provider | Version | Purpose | Confidence | Source |
|---|---|---|---|---|
| `azurerm` | `~> 3.0` or `~> 4.0` | Azure Resource Manager Terraform Provider | HIGH | [Terraform Registry: azurerm](https://registry.terraform.io/providers/hashicorp/azurerm/latest) |
| `random` | `~> 3.5` | Generates randomized suffix for globally unique storage account names | HIGH | [Terraform Registry: random](https://registry.terraform.io/providers/hashicorp/random/latest) |
| `terraform` | `>= 1.5.0` | Declarative IaC orchestration engine | HIGH | Terraform CLI (Local v1.15.8) |

## Patterns to Follow
- **Zero Secrets in Code**: No access keys or connection strings are stored or exported. Access is governed entirely by Microsoft Entra ID and RBAC via Managed Identity.
- **Content Hashing**: Use `content_md5 = filemd5("${path.module}/client_telemetry.csv")` in `azurerm_storage_blob` to detect changes and trigger automatic uploads.
- **Strict Naming Compliance**: Azure Storage accounts strictly forbid hyphens and uppercase characters; sanitize names to lowercase alphanumeric.

## Pitfalls to Avoid
- **Storage Account Name Collisions**: Azure Storage Account names are globally unique across all of Azure. Hardcoding an account name will fail provisioning; a random suffix must be appended.
- **Missing `features {}` Block**: The `azurerm` provider requires an empty `features {}` block in the provider declaration.
- **Over-Privileged Roles**: Use `Storage Blob Data Reader` rather than `Storage Blob Data Contributor` or `Owner` to ensure strict least privilege for the read-only MCP server.

---
*Researched: 2026-09-07*
