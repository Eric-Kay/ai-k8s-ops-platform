#!/bin/bash

set -e

echo "Scanning repository filesystem..."
trivy fs .

echo "Scanning Kubernetes manifests..."
trivy config k8s/

echo "Scanning Terraform..."
trivy config terraform/