#### AUTH && PLUGIN

terraform {
  required_providers {
    ibm = {
      source  = "IBM-Cloud/ibm"
      version = "~> 1.12.0"
    }
  }
}


provider "ibm" {}

#### RESOURCE GROUP

data "ibm_resource_group" "group" {
  name = "fpe_insper"
}

#### Machine learning service
resource "ibm_resource_instance" "wml" {
  name              = "TESTE_TERRAFORM"
  service           = "pm-20"
  plan              = "lite"
  location          = "us-south"
  resource_group_id = data.ibm_resource_group.group.id
  tags              = ["TESTE", "TERRAFORM"]

}

#### Object storage

resource "ibm_resource_instance" "cos" {
  name              = "TESTE_COS"
  service           = "cloud-object-storage"
  plan              = "standard"
  location          = "global"
  resource_group_id = data.ibm_resource_group.group.id
  tags              = ["TERRAFORM", "TEST"]

}
