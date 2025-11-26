resource "google_project_service" "run_api" {
  service = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_cloud_run_v2_service" "sample-service" {
  name     = var.cloudrun_service_name
  location = var.region
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"

  scaling {
    max_instance_count = 100
  }

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
    }
  }

  lifecycle {
    # Ignore changes to image, because Cloud Build will update the image later.
    # This prevents Terraform from downgrading the image version back to hello-world.
    ignore_changes = [
      template[0].containers[0].image,
      client,
      client_version
    ]
  }

  depends_on = [google_project_service.run_api]
}

resource "google_cloud_run_v2_service_iam_member" "noauth" {
  location = google_cloud_run_v2_service.sample-service.location
  name     = google_cloud_run_v2_service.sample-service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}