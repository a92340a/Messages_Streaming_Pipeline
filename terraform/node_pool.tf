resource "google_container_node_pool" "my_nodes" {
  project    = var.project_id
  name       = "default-pool"
  cluster    = google_container_cluster.my_cluster.id
  initial_node_count = 3
  location   = var.location

  autoscaling {
    location_policy      = "ANY"
    max_node_count       = 0
    min_node_count       = 0
    total_max_node_count = 5
    total_min_node_count = 0
  }

  node_config {
    machine_type = "n2-standard-2"
    service_account = "default"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
  depends_on = [google_container_cluster.my_cluster]
}