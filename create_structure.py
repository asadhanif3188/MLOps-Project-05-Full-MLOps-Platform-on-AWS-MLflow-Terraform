import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

# ----------------------------------------------------
# Directory + file structure for full MLOps platform
# ----------------------------------------------------

list_of_paths = [

    # Root folders
    "infra/terraform/envs/dev/main.tf",
    "infra/terraform/envs/dev/variables.tf",
    "infra/terraform/envs/dev/backend.tf",
    "infra/terraform/envs/dev/terraform.tfvars",

    # "infra/terraform/envs/prod/main.tf",
    # "infra/terraform/envs/prod/variables.tf",
    # "infra/terraform/envs/prod/backend.tf",
    # "infra/terraform/envs/prod/terraform.tfvars",

    # Terraform modules
    # "infra/terraform/modules/vpc/.gitkeep",
    # "infra/terraform/modules/eks/.gitkeep",
    # "infra/terraform/modules/node_group/.gitkeep",
    # "infra/terraform/modules/s3/.gitkeep",
    # "infra/terraform/modules/rds/.gitkeep",
    # "infra/terraform/modules/ecr/.gitkeep",
    # "infra/terraform/modules/cloudwatch/.gitkeep",
    # "infra/terraform/modules/iam/.gitkeep",

    # Helm
    # "infra/helm/mlflow/.gitkeep",
    # "infra/helm/inference-api/.gitkeep",

    # MLOps level
    # "mlops/mlflow/config/.gitkeep",
    # "mlops/mlflow/bootstrap_scripts/.gitkeep",

    # "mlops/pipelines/training/.gitkeep",
    # "mlops/pipelines/evaluation/.gitkeep",
    # "mlops/utils/.gitkeep",

    # Services
    # "services/inference-api/app/main.py",
    # "services/inference-api/app/model_loader.py",
    # "services/inference-api/Dockerfile",
    # "services/inference-api/requirements.txt",

    # "services/batch-jobs/train/.gitkeep",
    # "services/batch-jobs/feature-gen/.gitkeep",

    # GitHub workflows
    # ".github/workflows/infra-ci.yml",
    # ".github/workflows/app-ci.yml",
]

# ----------------------------------------------------
# File/Directory creation script
# ----------------------------------------------------

for path in list_of_paths:
    filepath = Path(path)
    filedir, filename = os.path.split(filepath)

    # Create directory if missing
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Directory created: {filedir}")

    # Create file if it doesn't exist or is empty
    if not filepath.exists() or filepath.stat().st_size == 0:
        with open(filepath, "w") as f:
            pass
        logging.info(f"Created empty file: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")
