output "frontend_url" {
  value = google_cloud_run_service.frontend.status[0].url
}

output "backend_url" {
  value = google_cloud_run_service.backend.status[0].url
}

output "backend_service_name" {
  value = google_cloud_run_service.backend.name
}

output "frontend_service_name" {
  value = google_cloud_run_service.frontend.name
}

output "artifact_registry_backend_repo" {
  value = google_artifact_registry_repository.backend_repo.repository_id
}

output "artifact_registry_frontend_repo" {
  value = google_artifact_registry_repository.frontend_repo.repository_id
}