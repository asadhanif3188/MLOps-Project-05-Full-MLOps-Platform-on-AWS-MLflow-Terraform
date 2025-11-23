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

## 2. Architecture

```text
                         GitHub
                   +----------------+
                   |  mono-repo     |
                   |  (infra+app)   |
                   +--------+-------+
                            |
                            | GitHub Actions (CI/CD)
                            v
+---------------------------------------------------------------+
|                           AWS Account                         |
+--------------------------+------------------------------------+
                           |
                           v
                  +--------+--------+
                  |       VPC       | 10.0.0.0/16
                  +--------+--------+
                           |
           +---------------+-----------------------------+
           |                                             |
   +-------+--------+                           +--------+--------+
   | Public Subnets |                           | Private Subnets |
   | (ALB, NAT GW)  |                           | (EKS, RDS)      |
   +-------+--------+                           +--------+--------+
           |                                             |
   +-------+-------+                           +---------+----------+
   |   ALB / NLB   |                           |       EKS Cluster  |
   | (MLflow, API) |                           |  (control plane)   |
   +-------+-------+                           +---------+----------+
           |                                             |
   +-------+--------+                    +--------------+-------------------+
   |   MLflow UI    |                    | EKS Managed Node Groups          |
   | (inference API)|                    |----------------------------------|
   +----------------+                    | - general node group (CPU)       |
                                         | - gpu node group (GPU)          |
                                         +--------------+-------------------+
                                                        |
                                                        v
         +----------------------+       +----------------+-----------------+
         |    S3: mlops-data    |       |   RDS PostgreSQL (MLflow DB)    |
         |    S3: mlops-feat    |       +---------------------------------+
         | S3: mlops-artifacts  |
         +----------------------+

```

## 3. Repository Structure

```text
full-mlops-platform-aws-mlflow-terraform/
├─ infra/
│  ├─ terraform/
│  │  ├─ envs/
│  │  │  ├─ dev/
│  │  │  │  ├─ main.tf
│  │  │  │  ├─ variables.tf
│  │  │  │  ├─ backend.tf
│  │  │  │  └─ terraform.tfvars
│  │  │  └─ prod/
│  │  │     ├─ main.tf
│  │  │     ├─ variables.tf
│  │  │     ├─ backend.tf
│  │  │     └─ terraform.tfvars
│  │  ├─ modules/
│  │  │  ├─ vpc/
│  │  │  ├─ eks/
│  │  │  ├─ node_group/       # optional if you want custom mgmt
│  │  │  ├─ s3/
│  │  │  ├─ rds/
│  │  │  ├─ ecr/
│  │  │  ├─ cloudwatch/
│  │  │  └─ iam/
│  └─ helm/
│     ├─ mlflow/
│     └─ inference-api/
│
├─ mlops/
│  ├─ mlflow/
│  │  ├─ config/
│  │  └─ bootstrap_scripts/
│  ├─ pipelines/
│  │  ├─ training/
│  │  └─ evaluation/
│  └─ utils/
│
├─ services/
│  ├─ inference-api/
│  │  ├─ app/
│  │  │  ├─ main.py
│  │  │  └─ model_loader.py
│  │  ├─ Dockerfile
│  │  └─ requirements.txt
│  └─ batch-jobs/
│     ├─ train/
│     └─ feature-gen/
│
└─ .github/
   └─ workflows/
      ├─ infra-ci.yml
      └─ app-ci.yml
```

## 4. Prerequisites
- AWS account
- Terraform >= 1.5
- kubectl & awscli
- GitHub repository with OIDC → AWS role configured
- Domain + Route53 (for pretty MLflow & API URLs)

## 5. CI/CD
- `infra-ci.yml`:
    - On push: Terraform fmt/validate/plan
    - Manual approval → apply
- `app-ci.yml`:
        - On push to main: build + push Docker, deploy to EKS

## 6. Observability
- Logs: CloudWatch (`/aws/mlops/*`, Container Insights)
- Alarms:
    - ALB 5xx
    - GPU node CPU

## 7. Security & Cost
- IRSA for MLflow, inference API, and CronJobs
- Separate dev vs prod envs
- GPU node autoscaling, small RDS in dev, log retention

## 8. Future Improvements
- Use PyTorch/TensorFlow GPU models
- Add feature store (Feast, etc.)
- Add Argo Workflows / Airflow for orchestration
- Add Argo Rollouts for automated canary deployment