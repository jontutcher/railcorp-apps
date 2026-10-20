#!/usr/bin/env bash
# Build and push the upstream-based demo images with the OCI source labels the
# migrator reads. Usage: ./build.sh [registry/prefix] [platform]
set -euo pipefail
REG="${1:-reg.jtut.io/railcorp}"
PLATFORM="${2:-linux/arm64}"
REV="$(git rev-parse HEAD)"
SRC="https://github.com/jontutcher/railcorp-apps"
for app in ingest departures; do
  docker buildx build --platform "$PLATFORM" --push \
    --label "org.opencontainers.image.source=$SRC" \
    --label "org.opencontainers.image.revision=$REV" \
    --label "dev.chainguard.dockerfile=$app/Dockerfile" \
    --label "dev.chainguard.context=$app" \
    -t "$REG/$app:upstream" -t "$REG/$app:$REV" "$app"
  echo "$app -> $(crane digest "$REG/$app:upstream")"
done
