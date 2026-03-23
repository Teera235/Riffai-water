terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  backend "gcs" {
    bucket = "riffai-terraform-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  default = "riffai-platform"
}

variable "region" {
  default = "asia-southeast1"
}

# Cloud SQL (PostgreSQL + PostGIS)
resource "google_sql_database_instance" "riffai_db" {
  name             = "riffai-postgres"
  database_version = "POSTGRES_15"
  region           = var.region
  
  settings {
    tier = "db-custom-2-4096"
    
    database_flags {
      name  = "max_connections"
      value = "100"
    }
    
    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }
    
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.riffai_vpc.id
    }
  }
  
  deletion_protection = true
}

# VPC Network
resource "google_compute_network" "riffai_vpc" {
  name                    = "riffai-vpc"
  auto_create_subnetworks = false
}

# Cloud Storage Buckets
resource "google_storage_bucket" "satellite_data" {
  name     = "riffai-satellite-data"
  location = var.region
  
  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }
  
  versioning {
    enabled = true
  }
}
