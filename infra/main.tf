# ============================================================================
# Semantic Search - Terraform IaC
# ============================================================================

terraform {
  required_version = ">= 1.5"

  required_providers {
    huaweicloud = {
      source  = "huaweicloud/huaweicloud"
      version = "~> 1.83"
    }
  }

  backend "local" {}
}

provider "huaweicloud" {
  region = var.region
}

# ============================================================================
# Variables
# ============================================================================

variable "region" {
  description = "Huawei Cloud Region"
  type        = string
  default     = "cn-north-4"
}

variable "project_name" {
  description = "Project Name"
  type        = string
  default     = "semantic-search"
}

variable "project_id" {
  description = "Huawei Cloud Project ID"
  type        = string
  default     = ""
}

variable "availability_zone" {
  description = "Availability Zone"
  type        = string
  default     = "cn-north-4a"
}

# ============================================================================
# Network Resources
# ============================================================================

resource "huaweicloud_vpc" "main" {
  name                  = "${var.project_name}-vpc"
  cidr                  = "10.0.0.0/16"
}

resource "huaweicloud_vpc_subnet" "main" {
  name       = "${var.project_name}-subnet"
  vpc_id     = huaweicloud_vpc.main.id
  cidr       = "10.0.1.0/24"
  gateway_ip = "10.0.1.1"
}

resource "huaweicloud_networking_secgroup" "main" {
  name        = "${var.project_name}-sg"
  description = "Semantic Search Security Group"
}

resource "huaweicloud_networking_secgroup_rule" "ingress_http" {
  direction         = "ingress"
  ethertype        = "IPv4"
  protocol         = "tcp"
  port_range_min   = 80
  port_range_max   = 443
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = huaweicloud_networking_secgroup.main.id
}

resource "huaweicloud_networking_secgroup_rule" "ingress_8080" {
  direction         = "ingress"
  ethertype        = "IPv4"
  protocol         = "tcp"
  port_range_min   = 8080
  port_range_max   = 8080
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = huaweicloud_networking_secgroup.main.id
}

# ============================================================================
# CSS (Cloud Search Service)
# ============================================================================

resource "huaweicloud_css_cluster" "main" {
  name            = "${var.project_name}-css"
  engine_version  = "2.3.0"
  flavor          = "ess.spec-2u4g"
  instance_number = 1
  subnet_id       = huaweicloud_vpc_subnet.main.id
  security_group_id = huaweicloud_networking_secgroup.main.id
  volume {
    type = "HIGH"
    size = 100
  }
}

# ============================================================================
# CCE (Cloud Container Engine) - Replaced FunctionGraph
# ============================================================================

resource "huaweicloud_cce_cluster" "main" {
  name                  = "${var.project_name}-cce"
  cluster_type          = "VirtualMachine"
  flavor_id             = "cce.s1.small"
  vpc_id                = huaweicloud_vpc.main.id
  subnet_id             = huaweicloud_vpc_subnet.main.id
  container_network_type = "overlay_l2"
  container_network_cidr = "10.0.2.0/16"

  security_cluster_toggle  = "false"
  security_cluster_authtype = "rbac"

  tags = {
    project = var.project_name
  }
}

resource "huaweicloud_cce_node" "main" {
  cluster_id        = huaweicloud_cce_cluster.main.id
  name             = "${var.project_name}-node"
  flavor_id        = "s6.large.2"
  availability_zone = var.availability_zone
  subnet_id        = huaweicloud_vpc_subnet.main.id

  root_volume {
    size       = 40
    vol_type   = "SSD"
  }

  data_volumes {
    size       = 100
    vol_type   = "SSD"
  }

  tags = {
    project = var.project_name
  }
}

# ============================================================================
# APIG - Updated to route to CCE backend service
# ============================================================================

resource "huaweicloud_apig_instance" "main" {
  name                  = "${var.project_name}-apig"
  edition               = "BASIC"
  description           = "Semantic Search API Gateway"
  vpc_id                = huaweicloud_vpc.main.id
  subnet_id             = huaweicloud_vpc_subnet.main.id
  available_zone_ids    = [var.availability_zone]
}

resource "huaweicloud_apig_group" "main" {
  name        = "${var.project_name}-group"
  instance_id = huaweicloud_apig_instance.main.id
  description = "Semantic Search API Group"
}

# APIG Backend - points to CCE Node IP (to be configured after deployment)
resource "huaweicloud_apig_backend" "main" {
  instance_id  = huaweicloud_apig_instance.main.id
  name        = "${var.project_name}-backend"
  description = "CCE Backend Service"
  protocol    = "HTTP"
  host        = var.backend_host
  port        = 80
}

# APIG API - /search endpoint
resource "huaweicloud_apig_api" "search" {
  instance_id  = huaweicloud_apig_instance.main.id
  group_id     = huaweicloud_apig_group.main.id
  name        = "${var.project_name}-search"
  description = "Semantic search API"
  method      = "POST"
  path        = "/search"
  protocol    = "HTTP"

  request_params {
    name     = "body"
    type     = "REQUEST_BODY"
    required = "true"
    location = "BODY"
  }

  backend_params {
    type     = "REQUEST_BODY"
    name     = "body"
    value    = "body"
    location = "BODY"
    to       = "request"
  }

  backend_id = huaweicloud_apig_backend.main.id

  response {
    code         = 200
    description  = "Success"
    example      = "{\"success\": true}"
  }
}

# APIG API - /chat endpoint
resource "huaweicloud_apig_api" "chat" {
  instance_id  = huaweicloud_apig_instance.main.id
  group_id     = huaweicloud_apig_group.main.id
  name        = "${var.project_name}-chat"
  description = "RAG chat API"
  method      = "POST"
  path        = "/chat"
  protocol    = "HTTP"

  request_params {
    name     = "body"
    type     = "REQUEST_BODY"
    required = "true"
    location = "BODY"
  }

  backend_params {
    type     = "REQUEST_BODY"
    name     = "body"
    value    = "body"
    location = "BODY"
    to       = "request"
  }

  backend_id = huaweicloud_apig_backend.main.id

  response {
    code         = 200
    description  = "Success"
    example      = "{\"success\": true}"
  }
}

# ============================================================================
# Outputs
# ============================================================================

output "vpc_id" {
  description = "VPC ID"
  value       = huaweicloud_vpc.main.id
}

output "subnet_id" {
  description = "Subnet ID"
  value       = huaweicloud_vpc_subnet.main.id
}

output "security_group_id" {
  description = "Security Group ID"
  value       = huaweicloud_networking_secgroup.main.id
}

output "css_endpoint" {
  description = "CSS Endpoint"
  value       = huaweicloud_css_cluster.main.endpoint
  sensitive   = true
}

output "apig_url" {
  description = "APIG URL"
  value       = huaweicloud_apig_instance.main.ip
}

output "apig_instance_id" {
  description = "APIG Instance ID"
  value       = huaweicloud_apig_instance.main.id
}

output "apig_group_id" {
  description = "APIG Group ID"
  value       = huaweicloud_apig_group.main.id
}

output "cce_cluster_id" {
  description = "CCE Cluster ID"
  value       = huaweicloud_cce_cluster.main.id
}

output "cce_cluster_name" {
  description = "CCE Cluster Name"
  value       = huaweicloud_cce_cluster.main.name
}

output "cce_endpoint" {
  description = "CCE API Server Endpoint (use for kubectl)"
  value       = huaweicloud_cce_cluster.main.endpoint
}

output "cce_cluster_ca_cert" {
  description = "CCE Cluster CA Certificate (base64)"
  value       = huaweicloud_cce_cluster.main.certificate_authority[0].data
  sensitive   = true
}
