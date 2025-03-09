variable "project_id" {
  type        = string
  default     = "tw-rd-de-finn"
  description = "The project ID to host the cluster in"
}

variable "project_number" {
  type        = string
  default     = "365750068155"
  description = "The project number to host the cluster in"
}

variable "region" {
  type        = string
  default     = "asia-east1"
  description = "The region to host the cluster in"
}

variable "zone" {
  type        = string
  default     = "asia-east1-a"
  description = "The zone to host the cluster in"
}


variable "location" {
  type        = string
  default     = "asia-east1-a"
  description = "The location to host the cluster in (zonal)"
}
