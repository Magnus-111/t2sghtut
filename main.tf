terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.1.0"
    }
  }
}
provider "azurerm" {
  features {}
  resource_provider_registrations = "none"
}

terraform {
  backend "azurerm" {
    resource_group_name  = "rg-CezaryJ"
    storage_account_name = "sacezaryj"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

resource "azurerm_service_plan" "example" {
  name                = "cezaryj-app-service-plan"
  location            = "polandcentral"
  resource_group_name = "rg-CezaryJ"
  os_type             = "Linux"
  sku_name            = "P0v3"
}

resource "azurerm_linux_web_app" "example" {
  name                = "webapp-cezaryj-t2s-workshop-1"
  location            = "polandcentral"
  resource_group_name = "rg-CezaryJ"
  service_plan_id     = azurerm_service_plan.example.id
  site_config {}
}

resource "azurerm_storage_account" "qrcode" {
  name                     = "qrcode${random_id.qrcode.hex}"
  resource_group_name      = "rg-CezaryJ"
  location                 = "polandcentral"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "random_id" "qrcode" {
  byte_length = 4
}

resource "azurerm_storage_container" "qrcode" {
  name                  = "function-releases"
  storage_account_name  = azurerm_storage_account.qrcode.name
  container_access_type = "private"
}

resource "azurerm_function_app" "qrcode" {
  name                       = "qrcode-fn-cezaryj"
  location                   = "polandcentral"
  resource_group_name        = "rg-CezaryJ"
  app_service_plan_id        = azurerm_service_plan.example.id
  storage_account_name       = azurerm_storage_account.qrcode.name
  storage_account_access_key = azurerm_storage_account.qrcode.primary_access_key
  version                    = "~4"
  os_type                    = "linux"
  site_config {
    linux_fx_version = "PYTHON|3.9"
  }
  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME" = "python"
    "WEBSITE_RUN_FROM_PACKAGE" = "1"
  }
}
