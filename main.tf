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
