output "service_uri" {
  value = google_cloud_run_v2_service.sample-service.uri
}

output "service_status" {
  value = google_cloud_run_v2_service.sample-service.conditions
}

output "artifact_registry_repo" {
  value = google_artifact_registry_repository.my-repo.name
}

output "artifact_registry_registry_uri" {
  value = google_artifact_registry_repository.my-repo.registry_uri
}