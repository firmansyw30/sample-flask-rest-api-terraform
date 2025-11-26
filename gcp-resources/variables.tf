variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
  default     = "our-hull-385315"
}

variable "region" {
  description = "Google Cloud Region"
  default     = "us-central1"
}

variable "docker-repository" {
  description = "Artifact Registry Docker Repository Name"
  type        = string
  default     = "my-repository-1"
}

variable "uniform_bucket_level_access" {
  description = "Enable uniform bucket-level access for Cloud Storage bucket"
  type        = bool
  default     = true
}

variable "cloudrun_service_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default     = "cloudrun-service"
}