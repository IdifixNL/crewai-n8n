#!/bin/bash

# Backup n8n workflows to local storage (NOT git)
# Run this script periodically to keep workflows backed up locally

echo "🔄 Backing up n8n workflows..."

# Create flows directory if it doesn't exist
mkdir -p n8n-flows

# Export n8n data from Docker volume
docker run --rm \
  -v crewai_n8n_automation_n8n_data:/data \
  -v $(pwd)/n8n-flows:/backup \
  alpine:latest \
  sh -c "cp -r /data/workflows /backup/ 2>/dev/null || echo 'No workflows found'"

# If workflows exist, create timestamped backup
if [ -d "n8n-flows/workflows" ]; then
  BACKUP_DIR="$HOME/n8n-backups/$(date +%Y%m%d_%H%M%S)"
  mkdir -p "$BACKUP_DIR"
  cp -r n8n-flows/workflows "$BACKUP_DIR/"
  echo "✅ Workflows backed up to: $BACKUP_DIR"
  echo "🎉 n8n workflows backed up locally (not in git)!"
else
  echo "ℹ️ No workflows found to backup"
fi 