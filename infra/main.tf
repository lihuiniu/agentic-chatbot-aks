provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "agentic-rg"
  location = "East US"
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "agenticAksCluster"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "agentic-aks"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }
}