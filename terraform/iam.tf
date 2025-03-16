resource "google_service_account_iam_binding" "gke_workload_identity" {
  service_account_id = "projects/${var.project_id}/serviceAccounts/${var.project_number}-compute@developer.gserviceaccount.com"
  role               = "roles/iam.workloadIdentityUser"

  members = [
    "serviceAccount:${var.project_id}.svc.id.goog[default/default]"
  ]
  depends_on = [google_container_cluster.my_cluster]
}

resource "kubernetes_service_account" "spark" {
  metadata {
    name      = "spark"
    namespace = "default"
  }
}

# resource "kubernetes_service_account" "default" {
#   metadata {
#     name      = "default"
#     namespace = "default"
#     annotations = {
#       "iam.gke.io/gcp-service-account" = "${var.project_number}-compute@developer.gserviceaccount.com"
#     }
#   }
#   depends_on = [google_container_cluster.my_cluster]
# }

