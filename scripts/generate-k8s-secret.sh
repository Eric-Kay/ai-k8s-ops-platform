#!/bin/bash

set -e

DB_ENDPOINT=$1
DB_PASSWORD=$2

if [ -z "$DB_ENDPOINT" ] || [ -z "$DB_PASSWORD" ]; then
  echo "Usage: ./scripts/generate-k8s-secret.sh <db-endpoint> <db-password>"
  exit 1
fi

kubectl create namespace ai-k8s-ops --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic postgres-secret \
  --namespace ai-k8s-ops \
  --from-literal=POSTGRES_HOST="$DB_ENDPOINT" \
  --from-literal=POSTGRES_PORT="5432" \
  --from-literal=POSTGRES_DB="aik8sops" \
  --from-literal=POSTGRES_USER="aik8sadmin" \
  --from-literal=POSTGRES_PASSWORD="$DB_PASSWORD" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "PostgreSQL Kubernetes Secret created successfully."