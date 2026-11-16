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
