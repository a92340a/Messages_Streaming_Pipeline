resource "google_service_account_iam_binding" "gke_workload_identity" {
  service_account_id = "projects/${project_id}/serviceAccounts/${project_number}-compute@developer.gserviceaccount.com"
  role               = "roles/iam.workloadIdentityUser"

  members = [
    "serviceAccount:${project_id}.svc.id.goog[default/default]"
  ]
}

resource "kubernetes_service_account" "default" {
  metadata {
    name      = "default"
    namespace = "default"
    annotations = {
      "iam.gke.io/gcp-service-account" = "${project_number}-compute@developer.gserviceaccount.com"
    }
  }
}

