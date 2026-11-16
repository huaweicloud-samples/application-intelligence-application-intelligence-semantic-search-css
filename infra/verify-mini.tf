# ============================================================================
# Minimal Verification - VPC + APIG Only
# This is a quick validation config (1-2 min deployment)
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
  default     = "semantic-search-mini"
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
  description = "Security Group"
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

# ============================================================================
# APIG (Minimal - for verification only)
# ============================================================================

resource "huaweicloud_apig_instance" "main" {
  name                  = "${var.project_name}-apig"
  edition               = "BASIC"
  description           = "Verification APIG Instance"
  vpc_id                = huaweicloud_vpc.main.id
  subnet_id             = huaweicloud_vpc_subnet.main.id
  available_zone_ids    = [var.availability_zone]
}

resource "huaweicloud_apig_group" "main" {
  name        = "${var.project_name}-group"
  instance_id = huaweicloud_apig_instance.main.id
  description = "Verification API Group"
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

output "apig_instance_id" {
  description = "APIG Instance ID"
  value       = huaweicloud_apig_instance.main.id
}

output "apig_url" {
  description = "APIG URL"
  value       = huaweicloud_apig_instance.main.ip
}

output "apig_group_id" {
  description = "APIG Group ID"
  value       = huaweicloud_apig_group.main.id
}
