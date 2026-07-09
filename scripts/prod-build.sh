#!/usr/bin/env bash
set -euo pipefail

# --- 1. Configurations ---
IMAGE_NAME="ouslan/python-app"
IMAGE_TAG="${GITHUB_SHA:-latest}" # Defaults to 'latest' if not in GitHub Actions

echo "🚀 Starting Production Container Build Pipeline (via Podman)..."

# --- 2. Docker Hub Authentication ---
if [ -z "${DOCKER_PASSWORD:-}" ] || [ -z "${DOCKER_USERNAME:-}" ]; then
  echo "⚠️ Warning: DOCKER_USERNAME or DOCKER_PASSWORD not set. Skipping authentication."
else
  echo "🔐 Logging into Docker Hub..."
  # Podman expects the registry domain 'docker.io' explicitly for logins
  echo "$DOCKER_PASSWORD" | podman login docker.io -u "$DOCKER_USERNAME" --password-stdin
fi

# --- 3. Build & Push via Podman ---
echo "📦 Building image..."
podman build \
  --build-arg UV_VERSION="latest" \
  -t "docker.io/${IMAGE_NAME}:${IMAGE_TAG}" \
  -t "docker.io/${IMAGE_NAME}:latest" .

echo "📤 Pushing images to Docker Hub..."
podman push "docker.io/${IMAGE_NAME}:${IMAGE_TAG}"
podman push "docker.io/${IMAGE_NAME}:latest"

echo "✅ Deployment completed successfully!"
