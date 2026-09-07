output "resource_group_name" {
  description = "Name of the provisioned Azure Resource Group."
  value       = azurerm_resource_group.rg.name
}

output "storage_account_name" {
  description = "Name of the provisioned Azure Storage Account."
  value       = azurerm_storage_account.telemetry_storage.name
}

output "storage_container_name" {
  description = "Name of the Azure Blob Storage container."
  value       = azurerm_storage_container.telemetry_container.name
}

output "primary_blob_endpoint" {
  description = "Primary Blob Service endpoint URL."
  value       = azurerm_storage_account.telemetry_storage.primary_blob_endpoint
}

output "managed_identity_client_id" {
  description = "Client ID of the User Assigned Managed Identity with Storage Blob Data Reader permissions."
  value       = azurerm_user_assigned_identity.mcp_identity.client_id
}

output "telemetry_blob_name" {
  description = "Blob name of the uploaded client telemetry dataset."
  value       = azurerm_storage_blob.telemetry_blob.name
}
