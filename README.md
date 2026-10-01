# 🚀 DevSecOps Learning Repository

A comprehensive, production-ready DevSecOps pipeline built with GitHub Actions, integrating the full lifecycle of shift-left security scanning (SAST, SCA, IaC, Secrets, Container Security) into a modern Python/Flask + Kubernetes stack.

## 🔄 Pipeline Overview (Shift-Left Security)

The pipeline enforces security at every stage:

1.  🔐 **Secret Scanning**: Gitleaks - Scans for exposed secrets
2.  🧪 **SAST & Testing**: Bandit (Security) + Ruff (Linting) + Pytest (Unit Tests)
3.  📦 **SCA (Software Composition Analysis)**: pip-audit (Dependency Vulns) + Trivy (Filesystem Scan)
4.  🏗️ **IaC Scanning**: Trivy - Scans Kubernetes manifests for misconfigurations
5.  🐳 **Container Security**: Docker Build + Trivy Image Scan

## 📂 Project Structure

```
DevSecOps-learn/
├── demo-app/                   # Python Flask application
│   ├── app.py
│   ├── Dockerfile              # Multi-stage Docker build
│   ├── requirements.txt
│   └── tests/                  # Unit & security tests
├── k8s/                        # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ...
├── .github/workflows/          # GitHub Actions workflows
│   └── devsecops-pipeline.yml  # Main pipeline definition
├── .github/requirements.txt    # DevSecOps tools dependencies
├── .gitleaks.toml              # Gitleaks configuration
├── .trivy.yaml                 # Trivy configuration
├── ruff.toml                   # Ruff linting config
├── Makefile                    # Convenience scripts
├── DEVSECOPS.md                # This file
└── .gitignore                  # Security-relevant exclusions
```

## 🚀 Getting Started

### 1. Prerequisites

- A GitHub repository with the project files
- A Dockerfile for your application
- Kubernetes manifests in `k8s/` directory

### 2. Configure GitHub Actions

The pipeline is fully configured and ready to use:

```yaml
# .github/workflows/devsecops-pipeline.yml
name: DevSecOps Pipeline

on:
  push:
    branches: [main]
    paths:
      - "demo-app/**"
      - "k8s/**"
      - ".github/workflows/**"
  pull_request:
    branches: [main]
    paths:
      - "demo-app/**"
      - "k8s/**"
      - ".github/workflows/**"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  secret_scan:
    name: Secret Scanning (Gitleaks)
    # ... (rest of the pipeline)
```

### 3. Run the Pipeline

#### Manual Trigger

Go to your repository on GitHub → Actions → Select "DevSecOps Pipeline" → Click "Run workflow"

#### Automatic Triggers

- Push changes to `main` branch
- Open/Update a Pull Request targeting `main`

## 🛠️ Tools & Configuration

### Gitleaks

```toml
# .gitleaks.toml
[paths]
  ignore = ["""# Skip Terraform files as we are using a specific scanner
**/*.tf

# Skip Kubernetes configuration files which are handled separately
**/*.yaml
**/*.yml
"""]
```

### Trivy Configuration

```yaml
# .trivy.yaml
severity: ["CRITICAL", "HIGH", "MEDIUM"]
```

### Ruff Configuration

```toml
# ruff.toml
[lint]
extend-exclude = [
  # Exclude test files from linting
  "tests/",
  # Exclude Python package metadata files
  "**/__init__.py",
  "**/__version__.py"
]

[lint.select]
# Enable comprehensive linting rules
C901 = true  # Too complex functions
E = true   # Syntax errors
W = true   # Warning issues
F = true   # Bug risk
I = true   # Import order
PL = true  # Poorly formatted code
B = true   # Bug risk

[lint.ignore]
# Ignore specific rules that are too strict for this project
PLR0913 = true # Too many arguments in function
B005 = true    # Using 'str' as a type
```

### Makefile Shortcuts

```makefile
# Run full pipeline
.PHONY: pipeline
pipeline:
	@echo "Running DevSecOps Pipeline..."
	@gh workflow run devsecops-pipeline.yml -f main

# Run security scans locally
.PHONY: scan
scan:
	@echo "Running Security Scans..."
	@./.github/scripts/scan.sh

# Run tests
.PHONY: test
test:
	@echo "Running Tests..."
	@cd demo-app && pytest
```

## 🎯 Best Practices Implemented

### ✅ Concurrency Control

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Prevents duplicate pipeline runs on the same branch/PR, saving CI minutes.

### ✅ Principle of Least Privilege

```yaml
permissions:
  contents: read
```

Jobs default to read-only; write permissions are granted only where explicitly needed.

### ✅ Fail-Fast Security

Secret scanning and SAST run first. The pipeline fails immediately if vulnerabilities are detected, preventing insecure code from reaching production.

## 📊 Security Metrics

GitHub automatically aggregates security findings:

- **Secrets** → `Secrets` tab
- **SAST** → `Code Scanning` tab (SARIF format)
- **SCA** → `Code Scanning` tab (Trivy SARIF)
- **IaC** → `Code Scanning` tab (Trivy IaC)
- **Container** → `Code Scanning` tab (Trivy Container)

## 🧪 Testing

Run unit and security tests locally:

```bash
cd demo-app && pytest
```

Or use theMakefile:

```bash
make test
```

## 🚀 Deployment

Once the pipeline completes successfully:

1.  Ensure `push: false` is enabled in `docker/build-push-action`
2.  Push changes to main branch
3.  The pipeline will automatically build and push the Docker image
4.  Apply Kubernetes manifests:

    ```bash
    kubectl apply -k k8s/
    ```

## 📋 Security Checklist

- [ ] All manifests have resource limits and requests
- [ ] Secrets are stored in GitHub Secrets (not in code)
- [ ] No hardcoded credentials or API keys
- [ ] Docker images use non-root users
- [ ] Latest base images are used
- [ ] Security headers are enabled in Flask app
