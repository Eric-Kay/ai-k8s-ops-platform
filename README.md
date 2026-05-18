# AI Kubernetes Operations Platform

AI Kubernetes Operations Platform is a production-style Cloud, DevOps and Platform Engineering project.

It provides AI-assisted Kubernetes troubleshooting, stores incident analysis history in PostgreSQL, uses Terraform to provision AWS RDS, and deploys frontend/backend services to Kubernetes.

## Features

- AI-assisted Kubernetes incident analysis
- FastAPI backend
- Streamlit frontend
- PostgreSQL incident history
- AWS RDS provisioned with Terraform
- Kubernetes Secrets for database connectivity
- Dockerized frontend and backend
- Kubernetes manifests
- HPA autoscaling
- GitOps with Argo CD
- Monitoring with Prometheus and Grafana
- Security scanning with Trivy
- GitHub Actions CI/CD

## Architecture

```text
User
 ↓
Streamlit Frontend
 ↓
FastAPI Backend
 ↓
Kubernetes Logs / Events
 ↓
AI Troubleshooting Engine
 ↓
PostgreSQL RDS Incident History# ai-k8s-ops-platform
