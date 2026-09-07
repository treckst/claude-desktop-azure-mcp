variable "resource_group_name" {
  description = "Name of the Azure Resource Group hosting telemetry storage and identity resources."
  type        = string
  default     = "rg-claude-telemetry-bridge"
}

variable "location" {
  description = "Azure region where resources will be provisioned."
  type        = string
  default     = "francecentral"
}

variable "storage_account_prefix" {
  description = "Prefix for the Azure Storage Account name (must be 3-18 lowercase alphanumeric characters)."
  type        = string
  default     = "claudetel"
}

variable "blob_container_name" {
  description = "Name of the Azure Blob container storing client telemetry CSV datasets."
  type        = string
  default     = "client-workloads"
}

variable "telemetry_blob_name" {
  description = "Destination filename of the telemetry CSV inside the blob container."
  type        = string
  default     = "client_telemetry.csv"
}

variable "managed_identity_name" {
  description = "Name of the User Assigned Managed Identity used by Claude Desktop / MCP server."
  type        = string
  default     = "id-mcp-reader"
}
