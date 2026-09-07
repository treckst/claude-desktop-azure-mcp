terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "random_string" "sa_suffix" {
  length  = 6
  special = false
  upper   = false
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    Environment = "Internal"
    Project     = "ClaudeDesktopAzureTelemetryBridge"
    ManagedBy   = "Terraform"
  }
}

resource "azurerm_storage_account" "telemetry_storage" {
  name                     = "${lower(var.storage_account_prefix)}${random_string.sa_suffix.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
  is_hns_enabled           = false

  tags = {
    Environment = "Internal"
    Project     = "ClaudeDesktopAzureTelemetryBridge"
  }
}

resource "azurerm_storage_container" "telemetry_container" {
  name                  = var.blob_container_name
  storage_account_name  = azurerm_storage_account.telemetry_storage.name
  container_access_type = "private"
}

resource "azurerm_storage_blob" "telemetry_blob" {
  name                   = var.telemetry_blob_name
  storage_account_name   = azurerm_storage_account.telemetry_storage.name
  storage_container_name = azurerm_storage_container.telemetry_container.name
  type                   = "Block"
  source                 = "${path.module}/client_telemetry.csv"
  content_md5            = filemd5("${path.module}/client_telemetry.csv")
}

resource "azurerm_user_assigned_identity" "mcp_identity" {
  name                = var.managed_identity_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  tags = {
    Environment = "Internal"
    Project     = "ClaudeDesktopAzureTelemetryBridge"
  }
}

resource "azurerm_role_assignment" "mcp_storage_reader" {
  scope                = azurerm_storage_account.telemetry_storage.id
  role_definition_name = "Storage Blob Data Reader"
  principal_id         = azurerm_user_assigned_identity.mcp_identity.principal_id
}
