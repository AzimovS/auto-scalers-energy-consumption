# Generate random resource group name
resource "random_pet" "green" {
  separator = ""
  length    = 2
}

resource "azurerm_resource_group" "green" {
  name     = "green-${random_pet.green.id}"
  location = "northeurope"
  tags = {
    "description" = "terraform"
  }
}

resource "azurerm_kubernetes_cluster" "green" {
  location            = azurerm_resource_group.green.location
  name                = "aks-${random_pet.green.id}"
  tags = {
    "description" = "terraform"
  }
  resource_group_name = azurerm_resource_group.green.name
  dns_prefix          = "aks-${random_pet.green.id}"

  default_node_pool {
    name       = "default"
    vm_size    = "Standard_A2_v2"
    enable_auto_scaling = true
    min_count           = 1
    max_count           = 2
  }
  
  identity {
    type = "SystemAssigned"
  }
  
  linux_profile {
    admin_username = "ubuntu"

    ssh_key {
      key_data = jsondecode(azapi_resource_action.ssh_public_key_gen.output).publicKey
    }
  }
  
  network_profile {
    network_plugin    = "kubenet"
    load_balancer_sku = "standard"
  }
}

output "green_name" {
  value = azurerm_resource_group.green.name
}

output "green_location" {
  value = azurerm_resource_group.green.location
}

output "aks_name" {
  value = azurerm_kubernetes_cluster.green.name
}