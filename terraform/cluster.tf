# VPC-native Clusters

resource "google_container_cluster" "my_cluster" {
  name     = "cluster-1"
  project  = var.project_id
  location = var.location
  default_snat_status {
    disabled = false
  }
  service_external_ips_config {
    enabled = false
  }
  database_encryption {
    state = "DECRYPTED"
  }
  logging_config {
    enable_components = [
      "SYSTEM_COMPONENTS",
      "WORKLOADS",
    ]
  }
  monitoring_config {
    enable_components = [
      "SYSTEM_COMPONENTS",
      "STORAGE",
      "POD",
      "DEPLOYMENT",
      "STATEFULSET",
      "DAEMONSET",
      "HPA",
      "CADVISOR",
      "KUBELET",
    ]

    advanced_datapath_observability_config {
      enable_metrics = false
      enable_relay   = false
    }

    managed_prometheus {
      enabled = true
    }
  }

  master_authorized_networks_config {
    gcp_public_cidrs_access_enabled      = false
    private_endpoint_enforcement_enabled = false

    cidr_blocks {
      cidr_block   = "125.227.248.241/32"
      display_name = "cm"
    }
  }

  network_policy {
    enabled  = false
    provider = "PROVIDER_UNSPECIFIED"
  }
  notification_config {
    pubsub {
      enabled = false
    }
  }
  secret_manager_config {
    enabled = false
  }

  release_channel {
    channel = "REGULAR"
  }

  node_config {
    disk_size_gb                = 100
    disk_type                   = "pd-balanced"
    enable_confidential_storage = false
    image_type                  = "COS_CONTAINERD"
    labels                      = {}
    local_ssd_count             = 0
    logging_variant             = "DEFAULT"
    machine_type                = "e2-medium"
    metadata = {
      "disable-legacy-endpoints" = "true"
    }
    oauth_scopes = [
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
      "https://www.googleapis.com/auth/service.management.readonly",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/trace.append",
    ]
    preemptible = false
    resource_labels = {
      "goog-gke-node-pool-provisioning-model" = "spot"
    }
    resource_manager_tags = {}
    service_account       = "default"
    spot                  = true
    storage_pools         = []
    tags                  = []

    advanced_machine_features {
      enable_nested_virtualization = false
      threads_per_core             = 0
    }

    kubelet_config {
      allowed_unsafe_sysctls                 = []
      container_log_max_files                = 0
      cpu_cfs_quota                          = false
      image_gc_high_threshold_percent        = 0
      image_gc_low_threshold_percent         = 0
      insecure_kubelet_readonly_port_enabled = "TRUE"
      pod_pids_limit                         = 0
    }

    shielded_instance_config {
      enable_integrity_monitoring = true
      enable_secure_boot          = false
    }
  }
}


