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
  description = "Availability Zone for CCE nodes"
  type        = string
  default     = "cn-north-4a"
}

variable "backend_host" {
  description = "CCE Backend Service IP/Domain (configure after kubectl apply)"
  type        = string
  default     = "10.0.2.0"
}
