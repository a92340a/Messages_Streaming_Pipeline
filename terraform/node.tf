
resource "google_container_node_pool" "my_node_pool" {
  name     = "default-pool"
  project  = var.project_id
  cluster  = google_container_cluster.my_cluster.name
  location = var.location

  queued_provisioning {
    enabled = false
  }
}
