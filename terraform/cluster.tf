provider "kubernetes" {
  host                   = "https://${google_container_cluster.my_cluster.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(google_container_cluster.my_cluster.master_auth.0.cluster_ca_certificate)
}

data "google_client_config" "default" {}

resource "google_container_cluster" "my_cluster" {
  name     = "cluster-1"
  project  = var.project_id
  location = var.location
  initial_node_count = 3
  deletion_protection = false

  workload_identity_config {
    workload_pool = "tw-rd-de-finn.svc.id.goog"
  }

  addons_config {
    gcs_fuse_csi_driver_config {
        enabled = true 
      } 
  }

  autoscaling {
      min_node_count = 1
      max_node_count = 5
  }

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
    
    cidr_blocks {
      cidr_block   = "42.77.243.251/32"
      display_name = "mobile"
    }
    
    cidr_blocks {
      cidr_block   = "180.177.8.10/32"
      display_name = "home"
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
    machine_type                = "n2-standard-2"
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


