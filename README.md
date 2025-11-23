# Full MLOps Platform on AWS (EKS + MLflow + Terraform)

## 1. Overview

This project implements a production-style MLOps platform on AWS:
- Terraform-provisioned VPC & EKS (with GPU node group)
- MLflow Tracking Server + Model Registry on EKS
- S3-based data & feature storage
- RDS PostgreSQL backend for MLflow
- Training & feature pipelines (Python) running as EKS CronJobs
- FastAPI inference service on GPU nodes
- CI/CD with GitHub Actions for infrastructure & applications
- CloudWatch-based logging & basic alerting

